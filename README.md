### FRC Rating System

---

A statistics website for FRC.

---

##### Developing for this Project
---

In order to develop for this project you will need to install a few development tools, namely `npm`, `bower`, `sass` and `typescript`. To install sass you will necessary need to install `ruby` to access `gem`. In order to maintain quality for scss files, you will also need `scss-lint` which is another ruby gem.

0. [`python3`](https://www.python.org/) : Python 3.x is required for this project, comes with the `pip` dependency manager
0. [`ruby`](https://www.ruby-lang.org/en/) : Ruby comes with support for installing ruby gems (sass requires this)
1. [`npm`](https://nodejs.org/en/) : Node.js comes with npm pre-packaged
2. [`bower`](http://bower.io/) : `npm install -g bower`
3. [`sass`](http://sass-lang.com/) : `gem install sass`
4. [`scss-lint`](https://github.com/brigade/scss-lint) : `gem install scss_list`
5. [`typescript`](https://www.typescriptlang.org/) : `npm install -g typescript`

After installing all the above dependencies you may proceed to execute the following commands to install python, javascript and css dependencies:

- `pip install -r requirements.txt`
- `npm install`
- `bower install`

Anytime `requirements.txt` is updated you will need to run the `pip` command above if your IDE does not notify you of these changes. Anytime `package.json` is updated you will need to run the `npm install` again. Anytime `bower.json` is updated you will need to run `bower install` again.

***When adding `npm` dependencies,*** run your command as follows (one or the other, not both):

- `npm install <dependency_name> --save`
- `npm install <dependency_name> --save-dev`

***When adding `bower` dependencies*,** run your command as follows (one or the other, not both):

- `bower install <dependency_name> --save`
- `bower install <dependency_name> --save-dev`


***When adding `pip` dependencies,*** run `pip freeze > requirements.txt` afterwards so that these dependencies can be consistent between developers.

##### Reference in this project:

[The Blue Alliance API v2](http://www.thebluealliance.com/apidocs)

---
###### Copyright (c) 2016 The FIRST Rating System Developers
