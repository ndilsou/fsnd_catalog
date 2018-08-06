INSERT INTO users VALUES (1, 'Admin', 'test@testmail.com');
INSERT INTO users VALUES (2, 'John Doe', 'jon.jon.doe@testmail.com');

INSERT INTO categories VALUES (1, 'Football', 'The real one from Europe.', 2);

INSERT INTO items VALUES (1, 'Football ball', 'Rather hard to play without one init?', 1);
INSERT INTO items VALUES (2, 'Arsenal Jersey', 'You still there Arsene?', 1);
INSERT INTO items VALUES (3, 'Drama Classes', 'Falling on the grass is an art. It takes ' ||
                                              'practice to master it.', 1);

INSERT INTO categories VALUES (2, 'Boxing', 'If you''re up for a good fight.', 2);

INSERT INTO items VALUES (4, 'Gloves', 'We''re fighters here, not brute.', 2);
INSERT INTO items VALUES (5, 'Jumping Rope', 'Just like Rocky.', 2);
