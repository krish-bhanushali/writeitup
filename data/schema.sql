drop table if exists notes;
drop table if exists catagories;

create table catagories (
  id integer primary key autoincrement,
  catagory_Name text not null,
  catagory_Color text not null
);

create table notes (
  id integer primary key autoincrement,
  title text not null,
  note text not null,
  dateOfNote text not null,
  catagoryOfNote int,
  FOREIGN KEY(catagoryOfNote) REFERENCES catagories(id)
);

