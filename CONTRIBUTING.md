**Be sure to have your editor of choice follow the standards laid out in the `.editorconfig` file.**

***When adding `npm` dependencies,*** run your command as follows (one or the other, not both):

- `npm install <dependency_name> --save`
- `npm install <dependency_name> --save-dev`

***When adding `bower` dependencies*,** run your command as follows (one or the other, not both):

- `bower install <dependency_name> --save`
- `bower install <dependency_name> --save-dev`


***When adding `pip` dependencies,*** run `pip freeze > requirements.txt` afterwards so that these dependencies can be consistent between developers.
