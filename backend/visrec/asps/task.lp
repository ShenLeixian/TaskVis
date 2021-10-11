% === Task - marktype correlations ===
:- task(retrieve_value), not mark(rect).
:- task(filter), not mark(rect), not mark(bar), not mark(arc).
:- task(compute_derived_value), not mark(rect), not mark(arc), not mark(bar).
:- task(find_extremum), not mark(bar),not mark(point).
:- task(sort), not mark(bar).
:- task(determine_range), not mark(tick),not mark(boxplot).
:- task(characterize_distribution), not mark(bar), not mark(point).
:- task(find_anomalies), not mark(bar), not mark(point).
:- task(cluster), not mark(bar), not mark(point).
:- task(correlate), not mark(bar), not mark(line), not mark(point).         
:- task(part_to_whole), not mark(arc).
:- task(change_over_time), not mark(line), not mark(area).
:- task(magnitude), not mark(arc), not mark(bar).
:- task(comparison), not mark(line),not mark(point),not mark(bar).
% :- task(spatial), not mark(circle).
:- task(spatial), not mark(geoshape),not mark(circle).
:- task(deviation), not mark(bar), not mark(point).
:- task(trend), not mark(point).
% :- task(bi_variate), not mark(line).
:- task(error_range), not mark(errorband), not mark(errorbar).
% @end

% task comprehensive
% @constraint should not bin/aggregate.
:- aggregate(_,_),task(determine_range;trend;deviation;error_range).
:- bin(_,_),task(retrieve_value;determine_range;correlate;cluster;change_over_time;find_anomalies;trend;spatial;deviation;error_range).
% @constraint should not use 'normalize' stack.
:- stack(_,normalize), task(retrieve_value;filter;find_extremum;find_anomalies;characterize_distribution;cluster;comparison;deviation).
:- stack(_,zero), task(characterize_distribution;find_anomalies;cluster;comparison;deviation).
% :- stack(_,center), task(retrieve_value;filter;find_extremum;find_anomalies;characterize_distribution;cluster;comparison;deviation).
% :- stack(_,null), task(retrieve_value;filter;find_extremum;find_anomalies;characterize_distribution;cluster;comparison;deviation).
% @constraint against c/s/s.
:- channel(_,(shape;size;color)), task(determine_range;deviation;error_range).
% @constraint allow 1 axis.
:- not channel(_,(x;y)),not task(determine_range),not mark(geoshape).

% task(retrieve_value)--------

% task(find_extremum)--------
% @constraint should not share the same var in x/y and c/s/s in FE task.
:- task(find_extremum),channel(N1,x),field(N1,F),channel(N2,(color;size;shape)),field(N2,F).
:- task(find_extremum),channel(N1,y),field(N1,F),channel(N2,(size;shape)),field(N2,F).
% @constraint should not display d_d in FE task.
:- task(find_extremum),is_d_d.

% task(compute_derived_value)--------
% @constraint must have bin/aggregate.
:- {aggregate(_,A): aggregate_op(A)}=0,{ bin(_,_)}=0, task(compute_derived_value).

% task(determine_range)--------
% @constraint can not have y.
% :- channel(_,y), task(determine_range).
% @constraint channel y(x) must be discrete(continuous).
:- channel_continuous(y), task(determine_range).
:- channel_discrete(x), task(determine_range).
% @constraint allow to use continuous on x, discrete on y.
:- channel_continuous(x), channel_discrete(y),not task(determine_range).


% task(characterize_distribution)--------
% @constraint only support count aggregate.
:- task(characterize_distribution),aggregate(_,_),not aggregate(_,count).

% task(find_anomalies)--------
% @constraint only support count aggregate.
:- task(find_anomalies),aggregate(_,_),not aggregate(_,count).

% task(cluster)--------
% @constraint must use discrete var in c/s/s.
:- channel(E,(shape;size;color)), type(E,quantitative), task(cluster).
% @constraint should have c/s.
:- not channel(_,color),not channel(_,shape),task(cluster).

% task(comparison)--------
% @constraint mark point/line must have c/s.
:- mark((point;line)),not channel(_,size),not channel(_,color),task(comparison).
% @constraint c/s/s can not be quantitative.
:- channel(E,(shape;size;color)),type(E,quantitative),task(comparison).
% @constraint against shape channel.
:- channel(_,shape),task(comparison).

% task(deviation)--------
% @constraint cardinality of x must equal num_rows.
% :- channel(E,x), enc_cardinality(E,C),not num_rows(C), task(deviation).

% task(sort)--------
% @constraint only sort task can sort.
:- sort(_,_),not task(sort).
% @constraint sort task must sort.
:- not sort(_,_), task(sort).
% @constraint sort only at x.
:- sort(E,_),not channel(E,x), task(sort).
% @constraint sort against bin.
:- sort(_,_),bin(_,_),task(sort).
% @constraint sort against normalize stack.
:- sort(_,_),stack(_,normalize),task(sort).

% task(trend)--------
% @constraint transform only for trend.
:- transform(_),not task(trend).
% @constraint transform only for trend.
:- not transform(_),task(trend).
% @constraint c/s against trend task.
:- channel(_,(shape;size)), task(trend).
% @constraint c/s/s against transform in trend task.
:- channel(_,color),transform(_), task(trend).
% @constraint must use number data type in trend task.
:- channel(E,(x;y)), not type(E,quantitative), not type(E,temporal),task(trend).

% task(spatial)--------
% @constraint x/y must be quantitative.
% :- channel(E,(x;y)), not type(E,quantitative), task(spatial).
% @constraint longitude and latitude field.
longitude(E):- field(E,("longitude";"long";"Longitude";"Long";"LONGITUDE";"经度")).
latitude(E):- field(E,("latitude";"lat";"Latitude";"Lat";"LATITUDE";"纬度")).
:-channel(E,x),not longitude(E), mark(circle),task(spatial).
:-channel(E,y),not latitude(E),mark(circle), task(spatial).
% @constraint long and lat must appear together.
:-channel(E1,x),longitude(E1),channel(E2,y),not latitude(E2).
:-channel(E1,x),not longitude(E1),channel(E2,y),latitude(E2).
% @constraint long and lat only show in task(spatial).
:-channel(E,x),longitude(E),not mark(circle).
:-channel(E,y),latitude(E),not mark(circle).
% @constraint long only in x and lat only in y.
:-channel(E,(y;color;size;shape)),longitude(E).
:-channel(E,(x;color;size;shape)),latitude(E).
% @constraint USMapID field.
usmap(E):- field(E,("USMapID")).
% :-channel(E,(x;y)), usmap(E),not task(spatial).
% @constraint about mark.
:-mark(geoshape), channel(E,x), not usmap(E).
% @constraint usmap only in geoshape.
:-channel(E,_), usmap(E),not mark(geoshape).
% @constraint usmap only in x.
:-channel(E,(y;size;shape;color)), usmap(E).
% @constraint usmap against count.
:-channel(E,x), usmap(E), aggregate(_,count).
:-channel(E,x), longitude(E), aggregate(_,count).
% @constraint circle only for spatial.
:- channel(_,y), mark(geoshape).
% @constraint must have color.
:- not channel(_,color), task(spatial).
% @constraint Non-d_d against aggregate c/s.
:- channel(E1,color),aggregate(E1,_),not is_d_d,not task(spatial).
% @constraint Prefer not to use non-positional channels until all positional channels are used.
:- channel(_,C), non_positional(C), not channel(_,(x;y)),not mark(geoshape).
% @constraint against overlap.
:- channel(E1,x),field(E1,F),cardinality(F,C1),num_rows(C2),C1<C2, not aggregate(_,_),channel(E2,color),not discrete(E2), task(spatial).



% task(change_over_time)--------
% @constraint x must be temporal.
:- channel(E,x), not type(E,temporal), task(change_over_time).
% @constraint aggregate only allow sum.
:- aggregate(_,(count)), task(change_over_time).
% @constraint continuous x against aggregate y.
:- channel(E1,x),channel(E2,y),type(E1,temporal),aggregate(E2,_),not bin(E1,_),not task(change_over_time).
% @constraint mark area against overlap.
:- mark((area;line)),channel(E,x),field(E,F),cardinality(F,C1),num_rows(C2),C1<C2, not aggregate(_,_), task(change_over_time).

% task(error_range)--------
% @constraint channel x(y) must be discrete(continuous).
:- channel_continuous(x), task(error_range).
:- channel_discrete(y), task(error_range).
















% % === Mark types ===

% % @constraint Continuous by continuous for point mark.
% :- is_c_c, mark(point).

% % @constraint Continuous by continuous for line mark.
% :- is_c_c, mark(line).

% % @constraint Continuous by continuous for area mark.
% :- is_c_c, mark(area).

% % @constraint Continuous by continuous for text mark.
% :- is_c_c, mark(text).

% % @constraint Continuous by continuous for tick mark.
% :- is_c_c, mark(tick).

% % @constraint Continuous by discrete for point mark.
% :- is_c_d, not no_overlap, mark(point).

% % @constraint Continuous by discrete for bar mark.
% :- is_c_d, not no_overlap, mark(bar).

% % @constraint Continuous by discrete for line mark.
% :- is_c_d, not no_overlap, mark(line).

% % @constraint Continuous by discrete for area mark.
% :- is_c_d, not no_overlap, mark(area).

% % @constraint Continuous by discrete for text mark.
% :- is_c_d, not no_overlap, mark(text).

% % @constraint Continuous by discrete for tick mark.
% :- is_c_d, not no_overlap, mark(tick).

% % @constraint Continuous by discrete for point mark with no overlap.
% :- is_c_d, no_overlap, mark(point).

% % @constraint Continuous by discrete for bar mark with no overlap.
% :- is_c_d, no_overlap, mark(bar).

% % @constraint Continuous by discrete for line mark with no overlap.
% :- is_c_d, no_overlap, mark(line).

% % @constraint Continuous by discrete for area mark with no overlap.
% :- is_c_d, no_overlap, mark(area).

% % @constraint Continuous by discrete for text mark with no overlap.
% :- is_c_d, no_overlap, mark(text).

% % @constraint Continuous by discrete for tick mark with no overlap.
% :- is_c_d, no_overlap, mark(tick).

% % === Channel rankings à la APT ===

% % @constraint Continuous on x channel.
% :- channel(E,x), continuous(E).

% % @constraint Continuous on y channel.
% :- channel(E,y), continuous(E).

% % @constraint Continuous on color channel.
% :- channel(E,color), continuous(E).

% % @constraint Continuous on size channel.
% :- channel(E,size), continuous(E).

% % @constraint Continuous on text channel.
% :- channel(E,text), continuous(E).

% % @constraint Ordered on x channel.
% :- channel(E,x), discrete(E), not type(E,nominal).

% % @constraint Ordered on y channel.
% :- channel(E,y), discrete(E), not type(E,nominal).

% % @constraint Ordered on color channel.
% :- channel(E,color), discrete(E), not type(E,nominal).

% % @constraint Ordered on size channel.
% :- channel(E,size), discrete(E), not type(E,nominal).

% % @constraint Ordered on text channel.
% :- channel(E,text), discrete(E), not type(E,nominal).

% % @constraint Ordered on row channel.
% :- channel(E,row), discrete(E), not type(E,nominal).

% % @constraint Ordered on column channel.
% :- channel(E,column), discrete(E), not type(E,nominal).

% % @constraint Nominal on x channel.
% :- channel(E,x), type(E,nominal).

% % @constraint Nominal on y channel.
% :- channel(E,y), type(E,nominal).

% % @constraint Nominal on color channel.
% :- channel(E,color), type(E,nominal).

% % @constraint Nominal on shape channel.
% :- channel(E,shape), type(E,nominal).

% % @constraint Nominal on text channel.
% :- channel(E,text), type(E,nominal).

% % @constraint Nominal on row channel.
% :- channel(E,row), type(E,nominal).

% % @constraint Nominal on column channel.
% :- channel(E,column), type(E,nominal).

% % @constraint Nominal on detail channel.
% :- channel(E,detail), type(E,nominal).

% % @constraint Interesting on x channel.
% :- channel(E,x), enc_interesting(E).

% % @constraint Interesting on y channel.
% :- channel(E,y), enc_interesting(E).

% % @constraint Interesting on color channel.
% :- channel(E,color), enc_interesting(E).

% % @constraint Interesting on size channel.
% :- channel(E,size), enc_interesting(E).

% % @constraint Interesting on shape channel.
% :- channel(E,shape), enc_interesting(E).

% % @constraint Interesting on text channel.
% :- channel(E,text), enc_interesting(E).

% % @constraint Interesting on row channel.
% :- channel(E,row), enc_interesting(E).

% % @constraint Interesting on column channel.
% :- channel(E,column), enc_interesting(E).

% % @constraint Interesting on detail channel.
% :- channel(E,detail), enc_interesting(E).

% % === Aggregations ===

% % @constraint Count as aggregate op.
% :- aggregate(E,count).

% % @constraint Sum as aggregate op.
% :- aggregate(E,sum).

% % @constraint Mean as aggregate op.
% :- aggregate(E,mean).

% % @constraint Median as aggregate op.
% :- aggregate(E,median).

% % @constraint Min as aggregate op.
% :- aggregate(E,min).

% % @constraint Max as aggregate op.
% :- aggregate(E,max).

% % @constraint Standard Deviation as aggregate op.
% :- aggregate(E,stdev).

% % === Stack ===

% % @constraint Zero base for stack op.
% :- stack(zero).

% % @constraint Normalize between groupbys as stack op.
% :- stack(normalize).

% % @constraint Rect mark for value tasks.
% :- task(value), mark(rect).

% % @constraint Point mark for summary tasks.
% :- task(summary), mark(point).

% % @constraint Bar mark for summary tasks.
% :- task(summary), mark(bar).

% % @constraint Line mark for summary tasks.
% :- task(summary), mark(line).

% % @constraint Area mark for summary tasks.
% :- task(summary), mark(area).

% % @constraint Text mark for summary tasks.
% :- task(summary), mark(text).

% % @constraint Tick mark for summary tasks.
% :- task(summary), mark(tick).

% % @constraint Rect mark for summary tasks.
% :- task(summary), mark(rect).

% % === Task - channel correlations ===

% % @constraint Continuous x for value tasks.
% :- task(value), channel(E,x), continuous(E), enc_interesting(E).

% % @constraint Continuous y for value tasks.
% :- task(value), channel(E,y), continuous(E), enc_interesting(E).

% % @constraint Continuous color for value tasks.
% :- task(value), channel(E,color), continuous(E), enc_interesting(E).

% % @constraint Continuous size for value tasks.
% :- task(value), channel(E,size), continuous(E), enc_interesting(E).

% % @constraint Continuous text for value tasks.
% :- task(value), channel(E,text), continuous(E), enc_interesting(E).

% % @constraint Discrete x for value tasks.
% :- task(value), channel(E,x), discrete(E), enc_interesting(E).

% % @constraint Discrete y for value tasks.
% :- task(value), channel(E,y), discrete(E), enc_interesting(E).

% % @constraint Discrete color for value tasks.
% :- task(value), channel(E,color), discrete(E), enc_interesting(E).

% % @constraint Discrete shape for value tasks.
% :- task(value), channel(E,shape), discrete(E), enc_interesting(E).

% % @constraint Discrete size for value tasks.
% :- task(value), channel(E,size), discrete(E), enc_interesting(E).

% % @constraint Discrete text for value tasks.
% :- task(value), channel(E,text), discrete(E), enc_interesting(E).

% % @constraint Discrete row for value tasks.
% :- task(value), channel(E,row), discrete(E), enc_interesting(E).

% % @constraint Discrete column for value tasks.
% :- task(value), channel(E,column), discrete(E), enc_interesting(E).

% % @constraint Continuous x for summary tasks.
% :- task(summary), channel(E,x), continuous(E), enc_interesting(E).

% % @constraint Continuous y for summary tasks.
% :- task(summary), channel(E,y), continuous(E), enc_interesting(E).

% % @constraint Continuous color for summary tasks.
% :- task(summary), channel(E,color), continuous(E), enc_interesting(E).

% % @constraint Continuous size for summary tasks.
% :- task(summary), channel(E,size), continuous(E), enc_interesting(E).

% % @constraint Continuous text for summary tasks.
% :- task(summary), channel(E,text), continuous(E), enc_interesting(E).

% % @constraint Discrete x for summary tasks.
% :- task(summary), channel(E,x), discrete(E), enc_interesting(E).

% % @constraint Discrete y for summary tasks.
% :- task(summary), channel(E,y), discrete(E), enc_interesting(E).

% % @constraint Discrete color for summary tasks.
% :- task(summary), channel(E,color), discrete(E), enc_interesting(E).

% % @constraint Discrete shape for summary tasks.
% :- task(summary), channel(E,shape), discrete(E), enc_interesting(E).

% % @constraint Discrete size for summary tasks.
% :- task(summary), channel(E,size), discrete(E), enc_interesting(E).

% % @constraint Discrete text for summary tasks.
% :- task(summary), channel(E,text), discrete(E), enc_interesting(E).

% % @constraint Discrete row for summary tasks.
% :- task(summary), channel(E,row), discrete(E), enc_interesting(E).

% % @constraint Discrete column for summary tasks.
% :- task(summary), channel(E,column), discrete(E), enc_interesting(E).
