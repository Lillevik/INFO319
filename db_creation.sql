CREATE TABLE IF NOT EXISTS Tweet(
  created_at INTEGER NOT NULL,
  id VARCHAR(50) NOT NULL,
  id_str VARCHAR(50) NOT NULL,
  text VARCHAR(150) NOT NULL,
  source VARCHAR(100) NOT NULL,
  truncated VARCHAR(50) NOT NULL,
  quoted_status_id VARCHAR(50) ,
  quoted_status_id_str VARCHAR(50) ,
  is_quote_status VARCHAR(50) ,
  quote_count DOUBLE ,
  reply_count DOUBLE ,
  retweet_count DOUBLE,
  favorite_count DOUBLE,
  favorited VARCHAR(50),
  retweeted VARCHAR(50),
  filter_level VARCHAR(50),
  lang VARCHAR(50),
  timestamp_ms VARCHAR(50),
  lat DOUBLE,
  lon DOUBLE,
  place_id VARCHAR(50) NOT NULL,
  user_id DOUBLE NOT NULL,
  FOREIGN KEY(place_id) REFERENCES Place(id),
  FOREIGN KEY(user_id) REFERENCES User(id),
  PRIMARY KEY (id)
);
--split--
CREATE TABLE IF NOT EXISTS Place(
  id VARCHAR(50) NOT NULL,
  url VARCHAR(100) NOT NULL,
  place_type VARCHAR(50) NOT NULL,
  name VARCHAR(50) NOT NULL,
  full_name VARCHAR(50) NOT NULL,
  country_code VARCHAR(50) NOT NULL,
  country VARCHAR(50) NOT NULL,
  bounding_box TEXT,
  PRIMARY KEY (id)
);
--split--
CREATE TABLE IF NOT EXISTS User(
  id DOUBLE NOT NULL,
  id_str DOUBLE NOT NULL,
  url TEXT,
  name VARCHAR(50) NOT NULL,
  screen_name VARCHAR(50) NOT NULL,
  location VARCHAR(50),
  description TEXT,
  verified VARCHAR(50),
  followers_count DOUBLE,
  friends_count DOUBLE,
  listed_count DOUBLE,
  favourites_count DOUBLE,
  statuses_count DOUBLE,
  created_at VARCHAR(50) NOT NULL,
  lang VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
)




