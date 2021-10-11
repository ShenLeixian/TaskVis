% ====== Expressiveness and Well-Formedness Constraints ======

% === Within Encodings ===

% @constraint Primitive type has to support data type.
:- type(E,quantitative), field(E,F), fieldtype(F,(string;boolean)).
:- type(E,temporal), field(E,F), not fieldtype(F,datetime).

% @constraint Can only bin quantitative or ordinal.
:- type(E,T), bin(E,_), T != quantitative, T != ordinal.

% @constraint Can only use log with quantitative.
% :- log(E), not type(E,quantitative).

% @constraint Can only use zero with quantitative.
% :- zero(E), not type(E,quantitative).

% @constraint Cannot use log scale with discrete (which includes binned).
% :- log(E), discrete(E).

% @constraint Cannot use log and zero together.
% :- log(E), zero(E).

% @constraint Cannot use log if the data is negative or zero.
% :- log(E), field(E,F), extent(F,MIN,_), MIN <= 0.

% @constraint Cannot bin and aggregate.
:- bin(E,_), aggregate(E,_).

% @constraint Oridnal only supports min, max, and median.
% :- type(E,ordinal), aggregate(E,A), A != min, A != max, A != median.

% @constraint Temporal only supports min and max.
% :- type(E,temporal), aggregate(E,A), A != min, A != max.

% @constraint Cannot aggregate nominal.
% :- aggregate(E,_), type(E,nominal).

% @constraint Detail cannot be aggregated.
% :- channel(E,detail), aggregate(E,_).

% @constraint Count has to be quantitative and not use a field.
% :- aggregate(E,count), field(E,_).
:- aggregate(E,count), not type(E,quantitative).
:- aggregate(E,_), channel(E,x).

% @constraint Shape requires discrete and not ordered (nominal). Using ordinal would't make a difference in Vega-Lite.
:- channel(E,shape), not type(E,nominal).

% @constraint Detail requires nominal.
% :- channel(E,detail), not type(E,nominal).

% @constraint Size implies order so nominal is misleading.
% :- channel(E,size), type(E,nominal).

% @constraint Do not use size when data is negative as size implies that data is positive.
% :- channel(E,size), enc_extent(E,MIN,MAX), MIN < 0, MAX > 0.

% === Across encodings and between encodings and marks ===

% @constraint Cannot use single channels twice.
:- single_channel(C), 3 { channel(_,C) }10.

% @constraint There has to be at least one encoding. Otherwise, the visualization doesn't show anything.
:- not encoding(_).

% @constraint Row and column require discrete.
% :- channel_continuous(row;column).

% @constraint Don't use row without y. Just using y is simpler.
% :- channel(_,row), not channel(_,y).

% @constraint Don't use column without x. Just using x is simpler.
% :- channel(_,column), not channel(_,x).

% @constraint All encodings (if they have a channel) require field except if we have a count aggregate.
:- not field(E,_), not aggregate(E,count), encoding(E).

% @constraint Count should not have a field. Having a field doesn't make a difference.
:- aggregate(E,count), field(E,_).

% @constraint Text mark requires text channel.
% :- mark(text), not channel(_,text).

% @constraint Text channel requires text mark.
% :- channel(_,text), not mark(text).

% @constraint Point, tick, and bar require x or y channel.
:- mark(point;bar), not channel(_,x), not channel(_,y).

% @constraint Line and area require x and y channel.
:- mark(line;area), not channel(_,(x;y)).

% @constraint Line and area cannot have two discrete.
:- mark(line;area), channel_discrete(x), channel_discrete(y).

% @constraint Bar and tick cannot have both x and y continuous.
:- mark(bar), channel_continuous(x), channel_continuous(y).

% @constraint Bar, tick, line, area require some continuous variable on x or y.
:- mark(bar;area;line), not channel_continuous(x), not channel_continuous(y).

% @constraint Bar and area mark requires scale of continuous to start at zero.
% :- mark(bar;area), channel(E,x), orientation(horizontal), not zero(E).
% :- mark(bar;area), channel(E,y), orientation(vertical), not zero(E).

% @constraint Shape channel requires point mark.
:- channel(_,shape), not mark(point).

% @constraint Size only works with some marks. Vega-Lite can also size lines, and ticks but that would violate best practices.
:- channel(_,size), not mark(point), not mark(text).

% @constraint Detail requires aggregation. Detail adds a field to the group by. Detail could also be used to add information to tooltips. We may remove this later.
% :- channel(_,detail), not aggregate(_,_).

% @constraint Do not use log for bar or area mark as they are often misleading. We may remove this rule in the future.
% :- mark(bar;area), log(E), channel(E,(x;y)).

% @constraint Rect mark needs discrete x and y.
:- mark(rect), not is_d_d.

% @constraint Don't use the same field on x and y.
:- { field(E,F) : channel(E,x); field(E,F) : channel(E,y) } >= 2, field(F).

% @constraint Don't use count on x and y.
:- channel(EX,x), channel(EY,y), aggregate(EX,count), aggregate(EY,count).

% @constraint If we use aggregation, then all continuous fields need to be aggeragted.
% :- aggregate(_,_), continuous(E), not aggregate(E,_).

% @constraint Don't use multi count.
% :- { aggregate(_,count) } = 2.
:- { aggregate(_,count) } >1.
:- { channel(_,color) } >1.
:- { channel(_,size) } >1.
:- { channel(_,shape) } >1.
% === Global properties ===

% @constraint Bars and area cannot overlap.
:- mark(bar;area), overlap.

% @constraint Rects shouldn't overlap. They are used for dioscrete heatmaps.
:- mark(rect), overlap.

% == Stacking ==

% @constraint Only use stacking for bar and area.
:- stack(_), not mark(bar), not mark(area).

% @constraint Don't stack if aggregation is not summative (summative are count, sum, distinct, valid, missing).
:- stack(E,_), aggregate(E,A), not summative_aggregate_op(A).

% @constraint Need to stack if we use bar, area with discrete color.
:- mark(bar;area), channel(E,color), discrete(E), not stack(_).

% @constraint Can only use stack if we also use discrete color, or detail.
% :- stack(_), not channel_discrete(color), not channel(_,detail).

% @constraint If we use stack and detail, we also have to use quantitative color.
% :- stack(_), channel(_,detail), not channel(_,color).
% :- stack(_), channel(_,detail), channel(E,color), not aggregate(E,_).

% @constraint Stack can only be on continuous.
:- stack(E,_), discrete(E).

% @constraint Stack can only be on x or y.
:- stack(E,_), not channel(E,x), not channel(E,y).

% @constraint Cannot use non positional continuous with stack unless it's aggregated.
:- stack(_), non_positional(C), channel(E,C), not aggregate(E,_), continuous(E).

% @constraint Vega-Lite currently supports 8 shapes/sizes.
:- channel(E,(shape;size)), enc_cardinality(E,C), C > 8.

% @constraint At most 20 categorical colors.
:- channel(E,color), discrete(E), enc_cardinality(E,C), C > 20.

% === Type checks ===

% @constraint Check mark.
:- mark(M), not marktype(M).

% @constraint Check types of encoding properties.
:- channel(_,C), not channel(C).
:- field(_,F), not field(F).
:- type(_,T), not type(T).
:- aggregate(_,A), not aggregate_op(A).
:- bin(_,B), not B >= 0.  % @constraint Bin has to be a natural number.

% @constraint Fieldtype has to be primitive type.
:- fieldtype(_,T), not primitive_type(T).

% @constraint Task has to be one of the tasks.
:- task(T), not tasks(T).

% @constraint Num_rows has to be larger than 0.
:- num_rows(S), S < 0.

% @constraint Cardinality has to be larger than 0.
:- cardinality(_,C), C < 0.

% @constraint Entropy has to be positive.
% :- entropy(_,E), E < 0.

% @constraint Extent only allowed for numbers (for now).
% :- extent(F,_,_), not fieldtype(F,number).

% @constraint Order has to be correct.
% :- extent(_,MIN,MAX), MIN > MAX.

% @constraint The name of a field cannot be the name of an encoding. This is to prevent errors coming from the shortcuts in define.lp.
:- encoding(N), field(N).


% Add new
% @constraint channel type consistency.
:- channel(N,C),field(N,F), field(E,F), type(N,T),not bin(E,_),not type(E,T).


% @constraint Non-number can not be mean.
:- not fieldtype(F,number),field(E,F), aggregate(E,(sum;mean)).

% @constraint can not bin the same var both in x/y and c/s/s.
:- bin(N,_),bin(E,_),field(N,F),field(E,F),channel(N,(color;size;shape)).

% @constraint can not aggregate var that will not show.
% :- field(E,F),aggregate(E,_),channel(N,_),not field(N,F).

% @constraint against without x channel
% :- channel(_,y), not channel(_,x).
% :- channel(_,x), not channel(_,y).
% :- not channel(_,(x;y)).
:- not channel(_,x).

% @constraint datatime type against c/s/s.
:- channel(E,(shape;size;color)),field(E,F),fieldtype(F,datetime).

% @constraint line/area mark for color/size channels.
% :- mark(line;area), channel(color;size),channel(_,(color;size)).

% @constraint pie mark.
:- mark(arc), channel(_,x),not channel(_,y).
:- mark(arc), channel(_,(color;size;shape)).
:- mark(arc), is_c_c.

% @constraint channel should not have only one cardinality.
:- channel(E,(shape;size;color)), discrete_cardinality(E,C), C < 2.
% :- channel(E,_), discrete_cardinality(E,C), C < 2.

% @constraint c/s/s can not share channel with x/y.
% :- channel(E1,(color;size;shape)),field(E1,F),channel(E2,(x;y)),field(E2,F),not bin(E2,_),not aggregate(E2,_),not bin(E1,_),not aggregate(E1,_).

% @constraint order c/s/s to get unique answer.
:- channel(N1,y),channel(N2,(shape;size;color)),N1>N2,obj_id(N1),obj_id(N2).
:- channel(N1,x),channel(N2,(shape;size;color)),N1>N2,obj_id(N1),obj_id(N2).
:- channel(N1,color),channel(N2,size),N1>N2,obj_id(N1),obj_id(N2).
:- channel(N1,size),channel(N2,shape),N1>N2,obj_id(N1),obj_id(N2).
:- channel(N1,size),channel(N2,shape),N1>N2,obj_id(N1),obj_id(N2).

:- channel(N1,y),channel(N2,(shape;size;color)),N1>N2,encode(N1),encode(N2).
:- channel(N1,x),channel(N2,(shape;size;color)),N1>N2,encode(N1),encode(N2).
:- channel(N1,color),channel(N2,size),N1>N2,encode(N1),encode(N2).
:- channel(N1,size),channel(N2,shape),N1>N2,encode(N1),encode(N2).
:- channel(N1,size),channel(N2,shape),N1>N2,encode(N1),encode(N2).

% @constraint c/s/s combination.
:- channel(E1,(shape;color)),channel(E2,size),field(E1,F),field(E2,F).
% :- channel(E1,shape),channel(E2,size),field(E1,F),field(E2,F).
% :- channel(E1,color),channel(E2,size),field(E1,F),field(E2,F).

% @constraint x/y can not have the same channel with c/s/s.
:- channel(E1,(shape;size;color)),channel(E2,(x;y)),field(E1,F),field(E2,F).

% % @constraint mark arc focus on one var.
:- mark(arc),channel(E1,x),channel(E2,y),field(E1,F1),field(E2,F2),F1!=F2.

% % @constraint stack against count(y).
:- channel(E,y),aggregate(E,count),stack(E,_).

% % @constraint stack .
:- stack(_,_),not channel(_,color).

% % @constraint mark line against discrete var.
:- channel(E,x),mark((line;area)),discrete(E).

% @constraint continuous x against aggregate y.
:- channel(E1,x),channel(E2,y),type(E1,quantitative),aggregate(E2,_),not bin(E1,_).

% @constraint aggregate var against css.
:- channel(E1,(shape;size;color)),channel(E2,y),aggregate(E2,_),not type(E1,nominal).

% @constraint Non-d_d against aggregate c/s.
% :- channel(E1,(shape;size;color)),aggregate(E1,_), is_c_c,not mark(point).
:- channel(E1,(shape;size)),aggregate(E1,_),not is_d_d.

% @constraint discrete c/s/s against sum/mean.
:- channel(E1,(shape;size;color)),aggregate(E,(sum;mean)),discrete(E).

% @constraint x/y field consistence.
:- channel(E1,_),channel(E2,_),field(E1,F),field(E2,F),obj_id(E2),encode(E1),bin(E2,_).
:- channel(E1,x),channel(E2,x),field(E1,F1),field(E2,F2),F1!=F2.
:- channel(E1,y),channel(E2,y),field(E1,F1),field(E2,F2),F1!=F2.

% @constraint is_d_d against no css.
:- is_d_d,not channel(_,shape),not channel(_,size),not channel(_,color).

% @constraint c/s/s must have the same field with x/y in rect.
:- channel(E1,(shape;size;color)),field(E1,F1),channel(E2,x),field(E2,F2),channel(E3,y),field(E3,F3),F1!=F2,F1!=F3, mark(rect).

% @constraint mark arc can not have high cardinality.
:- mark(arc),channel(E,(x;y)), discrete_cardinality(E,C), C >20.

% @constraint temporal against boxplot.
:- mark(boxplot),channel(E,(x;y)), type(E,temporal).

% @constraint mark boxplot against no_overlap.
:- mark(boxplot),num_rows(C),cardinality(F,C),channel(E,(x;y)),field(E,F).

% @constraint aggregate against stack without c/s/s.
:- aggregate(E,_),stack(E,_),not channel(_,shape),not channel(_,size),not channel(_,color).

% @constraint mark bar must show aggregate info if overlap.
:- mark(bar), channel(E1,x),channel(E2,y),enc_cardinality(E1,C),not num_rows(C),not aggregate(E2,_),not stack(_).

% @constraint cannot show aggregate info if no overlap.
:- channel(E1,x),channel(E2,y),enc_cardinality(E1,C),num_rows(C),aggregate(E2,_).

% @constraint mark line must show aggregate info if overlap.
:- mark(line), channel(E1,x),channel(E2,y), enc_cardinality(E1,C),C<15.

% @constraint must use encode(e) first.
:- channel(E1,x),obj_id(E1),encode(E2),not channel(E2,x).
:- channel(E1,y),obj_id(E1),encode(E2),not channel(E2,y),not aggregate(_,count).

% @constraint can not aggregate twice.
:- channel(E1,C), channel(E2,C), aggregate(E1,count), aggregate(E2,mean).
:- channel(E1,C), channel(E2,C), aggregate(E1,count), aggregate(E2,sum).
% :- channel(E1,C1), aggregate(E1,_), channel(E2,C1), not field(E2,_).

% @constraint Prefer time on x.
:- type(E,temporal), channel(E,_),not channel(E,x).

% @constraint Prefer not to overlap with DxD.
:- is_d_d, overlap.

% @constraint Prefer not to use size when the cardinality is large on x or y.
:- continuous(E), channel(_,size), enc_cardinality(E,C), C > 60, channel(E,(x;y)).

% @constraint Chart orientation for bar and tick (with and without bin). Binned fields have short labels if they are quantitative while otherwise labels can be long.
:- bin(E,_), type(E,quantitative), not channel(E,x).

% @constraint Aggregate should also have a discrete encoding to group by.
:- aggregate(_,_), not discrete(_).

% @constraint Prefer not to use multiple non-positional encoding channels.
:- {channel(_,C): non_positional(C)} > 2.

% @constraint Binned quantitative field should not have too low cardinality.
% :- type(E,quantitative), bin(E,_), enc_cardinality(E,C), C < 15.
:- bin(E,_), enc_cardinality(E,C), C < 15.

% @constraint Shape channel should not have too high cardinality.
:- channel(E,shape), discrete_cardinality(E,C), C > 5.

% @constraint Prefer not to use the same field three or more times.
:- field(F), { field(_,F) } >= 3.

% @constraint Prefer binning with at most 12 buckets.
:- bin(E,B), B > 12.

% @constraint Prefer binning with more than 7 buckets.
:- bin(E,B), B <= 7.