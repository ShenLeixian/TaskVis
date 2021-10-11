import pandas as pd
import numpy as np
from time import strptime
import re

date_regexes = [
    # Format:
        # MM*DD*YY(YY) where * ∈ {. - /}
    # Examples:
        # 12.24.2019
        # 12:24:2019
        # 12-24-2019
        # 12/24/2019
        # 1/24/2019
        # 07/24/2019
        # 1/24/20
    [['%m/%d/%Y', '%m/%d/%y'], "([1][0-2]|[0]?[1-9])[-.\/]([1|2][0-9]|[3][0|1]|[0]?[1-9])[-.\/]([1-9][0-9]{3}|[0-9]{2})"],
    # Format:
        # YY(YY)*MM*DD where * ∈ {. - /}
    # Examples:
        # 2019.12.24
        # 2019.12.24
        # 2019-12-24
        # 2019/12/24
        # 2019/1/24
        # 2019/07/24
        # 20/1/24
    [['%Y/%m/%d', '%y/%m/%d'], "([1-9][0-9]{3}|[0-9]{2})[-.\/]([1][0-2]|[0]?[1-9])[-.\/]([1|2][0-9]|[3][0|1]|[0]?[1-9])"],
    # Format:
        # DD*MM*YY(YY) where * ∈ {. - /}
    # Examples:
        # 24.12.2019
        # 24:12:2019
        # 24-12-2019
        # 24/12/2019
        # 24/1/2019
        # 24/07/2019
        # 24/1/20
    [['%d/%m/%Y', '%d/%m/%y'], "([1|2][0-9]|[3][0|1]|[0]?[1-9])[-.\/]([1][0-2]|[0]?[1-9])[-.\/]([1-9][0-9]{3}|[0-9]{2})"],
    # Formats:
        # DD*MMM(M)*YY(YY) where * ∈ {. - / <space>}
    # Examples:
        # 8-January-2019
        # 31 Dec 19
    [['%d/%b/%Y', '%d/%B/%Y', '%d/%b/%y', '%d/%B/%y'], "([1|2][0-9]|[3][0|1]|[0]?[1-9])[-.\/\s](January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-.\/\s]([1-9][0-9]{3}|[0-9]{2})"],
    # Format:
        # DD*MMM(M) where * ∈ {. - / <space>}
    # Examples:
        # 31-January
        # 1 Jul
    [['%d/%b', '%d/%B'], "([1|2][0-9]|[3][0|1]|[0]?[1-9])[-.\/\s](January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"],
    # Formats:
        # MMM(M)*DD*YYY(Y) where * ∈ {. - / <space>}
    # Examples:
        # January-8-2019
        # Dec 31 19
    [['%b/%d/%Y', '%B/%d/%Y', '%b/%d/%y', '%B/%d/%y'], "(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-.\/\s]([1|2][0-9]|[3][0|1]|[0]?[1-9])[-.\/\s]([1-9][0-9]{3}|[0-9]{2})"],
    # Format:
        # MMM(M)*DD where * ∈ {. - / <space>}
    # Examples:
        # January-31
        # Jul 1
    [['%b/%d', '%B/%d'], "(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-.\/\s]([1|2][0-9]|[3][0|1]|[0]?[1-9])"],
    # Format:
        # YYYY
    # Examples:
        # 18XX, 19XX, 20XX
    [["%Y"], "(1[8-9][0-9][0-9]|20[0-2][0-9])"]
]

def isdate(datum):
    try:
        if datum == '' or str(datum).isspace():
            return False

        for idx, regex_list in enumerate(date_regexes):
            regex = re.compile(regex_list[1])
            match = regex.match(str(datum))

            if match is not None:
                return True

    except Exception as e:
        print("regex error")
        pass

    return False

def get_counts(series: pd.Series) -> dict:
    """Counts the values in a series (with and without NaN, distinct).

    Args:
        series: Series for which we want to calculate the values.

    Returns:
        A dictionary with the count values (with and without NaN, distinct).
    """
    value_counts_with_nan = series.value_counts(dropna=False)
    value_counts_without_nan = (
        value_counts_with_nan.reset_index(
        ).dropna().set_index("index").iloc[:, 0]
    )

    distinct_count_with_nan = value_counts_with_nan.count()
    distinct_count_without_nan = value_counts_without_nan.count()

    return {
        "value_counts": value_counts_without_nan,  # Alias
        "value_counts_with_nan": value_counts_with_nan,
        "value_counts_without_nan": value_counts_without_nan,
        "distinct_count_with_nan": distinct_count_with_nan,
        "distinct_count_without_nan": distinct_count_without_nan,
    }


def is_boolean(series: pd.Series, series_description: dict) -> bool:
    """Is the series boolean type?

    Args:
        series: Series
        series_description: Series description

    Returns:
        True is the series is boolean type in the broad sense (e.g. including yes/no, NaNs allowed).
    """
    keys = series_description["value_counts_without_nan"].keys()
    if pd.api.types.is_bool_dtype(keys):
        return True
    elif (
        1 <= series_description["distinct_count_without_nan"] <= 2
        and pd.api.types.is_numeric_dtype(series)
        and series[~series.isnull()].between(0, 1).all()
    ):
        return True
    elif 1 <= series_description["distinct_count_without_nan"] <= 4:
        unique_values = set([str(value).lower() for value in keys.values])
        accepted_combinations = [
            ["y", "n"],
            ["yes", "no"],
            ["true", "false"],
            ["t", "f"],
        ]

        if len(unique_values) == 2 and any(
            [unique_values == set(bools) for bools in accepted_combinations]
        ):
            return True

    return False


def is_numeric(series: pd.Series, series_description: dict) -> bool:
    """Is the series numeric type?

    Args:
        series: Series
        series_description: Series description

    Returns:
        True is the series is numeric type (NaNs allowed).
    """
    return pd.api.types.is_numeric_dtype(series) and (
        series_description["distinct_count_without_nan"] >= 2
        #         >= config["vars"]["num"]["low_categorical_threshold"].get(int)
        or any(np.inf == s or -np.inf == s for s in series)
    )


def is_valid_date(str_):
    try:
        strptime(str_, "%Y-%m-%d")
        return True
    except:
        return False


def is_date(series) -> bool:
    """Is the variable of type datetime? Throws a warning if the series looks like a datetime, but is not typed as datetime64.

    Args:
        series: Series

    Returns:
        True if the variable is of type datetime.
    """
    is_date_value = pd.api.types.is_datetime64_dtype(series)
    if not is_date_value:
        is_date_value = is_valid_date(series[0])
    if not is_date_value:
        for data in series[0:20]:
            is_date_value = isdate(data)
            # print("{} is {}".format(data,is_date_value))
            if not is_date_value:
                break
    return is_date_value


def get_var_type(series: pd.Series) -> dict:
    """Get the variable type of a series.

    Args:
        series: Series for which we want to infer the variable type.

    Returns:
        The series updated with the variable type included.
    """

    series_description = {}

    try:
        series_description = get_counts(series)

        # When the inferred type of the index is just "mixed" probably the types within the series are tuple, dict,
        # list and so on...
        if series_description["value_counts_without_nan"].index.inferred_type.startswith("mixed"):
            raise TypeError("Not supported mixed type")

        if series_description["distinct_count_without_nan"] == 0:
            var_type1 = 'unknown'
        elif is_boolean(series, series_description):
            var_type1 = 'boolean'
        elif is_date(series):
            var_type1 = 'datetime'
        elif is_numeric(series, series_description):
            var_type1 = 'number'
        else:
            var_type1 = 'string'
    except TypeError:
        var_type1 = 'unknown'

    TypeMap = {
        'number': "quantitative",
        'unknown': "nominal",
        'datetime': "temporal",
        'string': "nominal",
        'boolean': "nominal"
    }

    var_type2=TypeMap[var_type1]
    if var_type1=='number':
        if series_description["distinct_count_without_nan"]<7 and series_description["distinct_count_without_nan"]>1 and len(series)>50:
            var_type2='ordinal'

    series_description.update({"type1": var_type1, "type2": var_type2})
    return series_description


# decide columntype
# def add_columnTypes(data):
#     NORMALTYPE_TO_VISTYPE = {
#         int: "quantitative",
#         str: "nominal",
#         float: "quantitative",
#         decimal.Decimal: "quantitative",
#         datetime.datetime: "temporal",
#         bytes: "quantitative",
#         bool: "nominal",
#         datetime.date: "temporal",
#         datetime.time: "temporal",
#     }
#     if not data:
#         return None
#     columnTypes = {}
#     if type(data) == list:
#         if type(data[0]) == dict:
#             for key in data[0].keys():
#                 if type(data[0][key]) in NORMALTYPE_TO_VISTYPE.keys():
#                     columnTypes[key] = NORMALTYPE_TO_VISTYPE[type(data[0][key])]
#                 else:
#                     columnTypes[key] = None
#             return columnTypes
#         else:
#             # 处理没有转成Json的数据
#             try:
#                 result = data[0]
#                 for field in [
#                     x for x in dir(result) if not x.startswith("_") and x != "metadata"
#                 ]:
#                     data = result.__getattribute__(field)
#                     try:
#                         columnTypes[field] = NORMALTYPE_TO_VISTYPE[type(data)]
#                     except:
#                         continue
#                 return columnTypes
#             except Exception as e:
#                 print(e)
#                 return None
#     elif type(data) == dict:
#         for key in data.keys():
#             di = {}
#             if type(data[key]) == list and type(data[key][0]) == dict:
#                 for k in data[key][0].keys():
#                     if type(data[key][0][k]) in NORMALTYPE_TO_VISTYPE.keys():
#                         di[k] = NORMALTYPE_TO_VISTYPE[type(data[key][0][k])]
#                     else:
#                         di[k] = None
#             columnTypes[key] = di
#         return columnTypes
#     else:
#         return None
