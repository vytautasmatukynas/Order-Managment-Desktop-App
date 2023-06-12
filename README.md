# Order-Managment-Dektop-App-Demo
Scaling is abit fkd up. "scaling" class fixes some scaling problems, but... just some. And maybe some threads are needed for adding new, updating and etc. that app won't freeze till SQL is loaded.

Simple order managment dekstop app, where you can store your orders.
App shows when orders are late, you can attach order files .xlm .pdf .jpg .png, add link to order docs folder, new/update/delete/open functions, print table, search table, check for updates and info (request link and compare version number in link to '__version__' in .py, if version is higher than app version, then download new app setup from googledrive link). There is 'create_db_table.py' that creates postgreSQL table for this app. 'style_retro.py' contains all style applied to this app.

![paveikslas](https://user-images.githubusercontent.com/51360361/235490470-9f45f2f8-ea43-4721-ab34-7ca659b10c33.png)

"Add New" window dialog:

![paveikslas](https://user-images.githubusercontent.com/51360361/235490756-e80a647b-4d12-418d-89e5-7e17064b9a2c.png)

Double click on row to show "Update" window dialog:

![paveikslas](https://user-images.githubusercontent.com/51360361/235490691-5eb52291-626e-4f4e-8f6b-7a89219519a0.png)

There is dialog window in menu-bar "Settings" section where you can add new combo-box items:

![paveikslas](https://user-images.githubusercontent.com/51360361/235490641-222ec688-3128-4012-a75a-275dadf53395.png)

There is tree-table to sort items by ORDER_NAME:

![paveikslas](https://user-images.githubusercontent.com/51360361/235490561-a1638bac-7700-450d-b78f-7ab8f92b1c4b.png)

There is search - first search line sorts items and only shows what you are searching, second search line select items in table:

![paveikslas](https://user-images.githubusercontent.com/51360361/235491350-0749d596-a5f4-4764-97ad-04ea857a7024.png)

![paveikslas](https://user-images.githubusercontent.com/51360361/235491424-6ffe9645-9e45-4c2e-9eec-958af608f07e.png)

Export your table to .xlsx .csv:

![paveikslas](https://user-images.githubusercontent.com/51360361/235491253-aee3316f-1392-4cb0-8af1-ecdfa4850023.png)

Print table:

![paveikslas](https://user-images.githubusercontent.com/51360361/235491207-d6e00afb-dda2-40f5-ade2-78fb109d42ac.png)






