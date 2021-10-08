Databosses Mini Amazon Project

Assingment for Duke CS 316

Group Members: 
- Caroline Levenson: Users Guru
- Clara Lyra: Social Guru
- Jennifer Shultz: Products Guru
- Julia Ziaee: Carts Guru
- Nicole Malpeli: Sellers Guru

We chose the standard project option.

Progress Report Milestone 2

Everyone worked together to sketch an E/R diagram and discuss big picture aspects of the project. 
- Julia spearheaded the creation of the relational schema. 
- Julia and Clara detailed the assumptions and logistics of the schema. 
- Clara and Jennifer focused on specifying the contents and constraints of the main tables. 
- Julia and Nicole focused on creating the triggers for what follows a product purchase. 
- Caroline created inputs for the CSVs to load onto our database.
- Caroline also debugged the SQL database creation and tested the sample data.
- Nicole and Caroline worked on the page by page design on the website. 

Our [Gitlab Repository] (https://gitlab.oit.duke.edu/databosses/mini-amazon-skeleton)

To Create and Load Data into Database:
~/shared/final/mini-amazon-skeleton/db$ dropdb amazon; createdb amazon; psql amazon -af create.sql~/shared/final/mini-amazon-skeleton/db$ dropdb amazon; createdb amazon; psql amazon -af create.sql
~/shared/final/mini-amazon-skeleton/db$ psql amazon -af load.sql
