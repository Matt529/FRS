### FRC Rating System

---

A statistics website for FRC.

---
##### Do we have incorrect or missing data? [Read this!](https://github.com/FRC-RS/FRS/blob/master/bad_data.md)
---
##### Developing for this Project
---

In order to develop for this project you will need to install a few development tools, namely `npm`, `bower`, `sass` and `typescript`. To install sass you will necessary need to install `ruby` to access `gem`. In order to maintain quality for scss files, you will also need `scss-lint` which is another ruby gem.

0. [`python3`](https://www.python.org/) : Python 3.x is required for this project, comes with the `pip` dependency manager
0. [`ruby`](https://www.ruby-lang.org/en/) : Ruby comes with support for installing ruby gems (sass requires this)
1. [`npm`](https://nodejs.org/en/) : Node.js comes with npm pre-packaged
2. [`bower`](http://bower.io/) : `npm install -g bower`
3. [`sass`](http://sass-lang.com/) : `gem install sass`
4. [`scss-lint`](https://github.com/brigade/scss-lint) : `gem install scss_lint`
5. [`typescript`](https://www.typescriptlang.org/) : `npm install -g typescript`

After installing all the above dependencies you may proceed to execute the following commands to install python, javascript and css dependencies:

- `pip install -r requirements.txt`
- `npm install`
- `bower install`

Anytime `requirements.txt` is updated you will need to run the `pip` command above if your IDE does not notify you of these changes. Anytime `package.json` is updated you will need to run the `npm install` again. Anytime `bower.json` is updated you will need to run `bower install` again.

---

##### Installing MariaDB / MySQL on Windows

1. Install [`MariaDB 10.1`](https://downloads.mariadb.org/).
2. Install [`Visual Studio Community 2015`](https://www.visualstudio.com/en-us/visual-studio-homepage-vs.aspx). Make sure to install all C++ and Python components.
3. Install [`MySQL Connector C 6.0.2`](https://dev.mysql.com/downloads/connector/c/6.0.html).
4. If `MySQL Connector C 6.0.2` was installed in `C:\Program Files\MySQL`, then move it to `C:\Program Files (x86)\MySQL`. You can either manually move the files or you can create a link. Either works.
5. Download [`mysqlclient-1.3.7-cp35-none-win_amd64.whl`](https://drive.google.com/file/d/0B5k0KOgTOwrhSk5JR3lkU1duREU/view?usp=sharing).
6. Install it using `pip install mysqlclient-1.3.7-cp35-none-win_amd64`.
7. Run `pip install mysqlclient`.
8. Type `mysql -u root -p` into your console, then `password`, and enter the following:
```
CREATE DATABASE `FRS` DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE USER 'FRS_user'@'localhost' IDENTIFIED BY 'password';
USE 'mysql';
GRANT ALL PRIVILEGES ON FRS.* TO 'FRS_user'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```
9. `python manage.py makemigrations` and `python manage.py migrate`.
10. Install [`Solr 4.10.2`](https://archive.apache.org/dist/lucene/solr/4.10.2/solr-4.10.2.zip) which acts as our search engine.
11. `python manage.py build_solr_schema > schema.xml`
12. Copy `schema.xml` to the directory of `Solr 4.10.2` under `example\solr\collection1\conf`
13. In the `Solr 4.10.2` directory, execute `bin\solr start`, it is recommended you add the `bin` directory to your path.
14. `python manage.py rebuild_index`, whenever changes are made to the search indices `update_index` must be executed to take effect.

---

Want to contribute? [Read here!](https://github.com/FRC-RS/FRS/blob/master/CONTRIBUTING.md)

##### Reference in this project:

[The Blue Alliance API v2](http://www.thebluealliance.com/apidocs)

---
###### Copyright (c) 2016 The FIRST Rating System Developers
