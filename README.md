# Simple database upgrade script

This repository contains the code for automatically upgrading a database given the presence of sql scripts in a formatted fashion.

### How do I use it?

1. Create ~/.pgpass

    `touch ~/.pgpass`

    with the contents resembling something like this:
    
    ```
    localhost:5432:exampledb:thivan:<password>
    localhost:*:*:thivan:<password>
    ```

2. Give the right permissions to pgpass

    `chmod 600 ~/.pgpass`

4. Create a databaseversion table with the SQL script located in:

    `utils/create_version_table.sql`

3. export environment variables: DB_USER, DATABASE, DB_HOST

4. Run the script:
    ![Running script](/img/example_run)