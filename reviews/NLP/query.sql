select id, replace(replace(concat_comments, 'cleaned', 'clean'), 'cleaning', 'clean') as concat_comments from (select id,
       regexp_replace(replace(replace(replace(concat_comments, $$'$$, ''), $$'$$, ''), $$'$$, ''), '[^a-zA-Z]', ' ',
                      'g') as concat_comments
from (
         select id,
                concat_ws(' ', comments,
                          private_feedback,
                          accuracy_comments,
                          checkin_comments,
                          cleanliness_comments,
                          communication_comments,
                          location_comments,
                          improve_comments,
                          value_comments,
                          love_comments) as concat_comments
         from reviews_airbnb
         where overall_rating < 3) s1 where concat_comments is not null)s2 where concat_comments not ilike '%automated posting%';


