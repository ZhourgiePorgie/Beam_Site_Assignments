# Beam_Site_Assignments
## How to use
* Create a Google Form (all questions **MUST** match exactly)
  * Have an item for `Name` which takes in a short answer
  * Have an item for `Drive` which takes in a Yes or No
  * Have an item for `Spanish` which takes in a Yes or No
  * Have an item for `Availabilities` which is a multiple choice grid.  Rows are site times and Columns are Yes or No
* Link this Google Form to a spreadsheet called `Availabilities(Responses)`
* Create another Google Spreadsheet called `Site_Leaders`
  * The first column is for staff members titled `Staff Members`
  * The second column is for site leaders titled `Site Leaders`
* Create another Google Spreadsheet called `Sites`
  * The first column is for the site names titled `Name`
  * The second column is for driving information titled `Driving` (Yes/No)
  * The third column is for spanish speaking information titled `Spanish` (Yes/No)
  * **VERY IMPORTANT!** Order of sites in this spreadsheet **MUST** be the same order as on the Google form
* Download all spread sheets as `Microsoft Excel (.xlsx)` files into the `Excel_Spreadsheets` folder

Navigate to the folder where this file is present.  This can be done in a terminal (if Mac) or git bash (if Windows).  Type `ls` to see all the files in the current folder and `cd [folder]` to move into the folder that you specify.  You can use `cd ..` to go out of the current folder you are in.  When you see the files in this repository, run `python BEAM.py`.  The program will print the sites and their list of members.  Additional rearranging may be necessary since this is only a preliminary mapping of sites to a list of members.
