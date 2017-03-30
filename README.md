# Simple database upgrade script

This repository contains the code for automatically upgrading a database given the presence of sql scripts in a formatted fashion.

### How do I use it?

1. Create ~/.pgpass

`touch ~/.pgpass`

```localhost:5432:exampledb:thivan:<password>
localhost:*:*:thivan:<password>
```

2. Give the right permissions to pgpass

`chmod 600 ~/.pgpass`

4. Create a databaseversion table with the SQL script located in:

`utils/create_version_table.sql`

3. export environment variables: DB_USER, DATABASE, DB_HOST

4. Run the script:
![Running script](https://www.dropbox.com/s/gkcl1yiowizaklf/Screenshot%202017-03-30%2013.01.16.png?dl=0)