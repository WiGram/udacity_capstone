# Purpose
In this project, we build an etl pipeline that extracts Udacity provided data stored in sas7bdat- and csv-files. The data is then transformed and subsequently loaded into a snowflake schema designed for flexible querying. Ultimately, we are building a data model that will give the client easy access to query their data. 

The tables in the snowflake schema will ultimately be loaded to an S3 bucket where data can be read from or in case loaded to a redshift cluster for further computations.

The client here may be anyone with an interest in immigration data, and the end purpose is to allow the client's analytics team to query the data ad hoc for simple analyses, or to integrate the data in a bigger flow to support automated analyses.

# Data and Source files
The data provided consists of a main data table holding all immigration information, and supplementing data tables that hold data on airports, world temperature, and demographics in US cities, respectively. Finally, a SAS-file documenting several, but not all, of the data in the immigration data set is used to translate codes and abbreviations in the immigratio data set which will be stored in separate tables.

The data sets are as follows:

- I94 Immigration Data: This data comes from the US National Tourism and Trade Office and is stored in a .sas7bdat-file.
- World Temperature Data: This dataset came from Kaggle. This data resides in a .csv-file. You can read more about it here.
- U.S. City Demographic Data: This data comes from OpenSoft. This data resides in a .csv-file. You can read more about it here.
- Airport Code Table: This is a simple table of airport codes and corresponding cities. This data resides in a .csv-file. It comes from here.

# Data Model

The data model covers taking the sourced data and normalising it by structuring the data into a star schema. 

As was covered in section 1 the data is loaded from several sources which will be further explained upon in the next section:
1. Immigration data
2. Temperature data
3. Demographics data
4. Airports data
5. Text file with documentation

![Image of Immigration Data Model]('imm_data.jpg')

There will be a heavy focus on field naming conventions to facilitate analysis. Thus we have some standards:
- CD: Fields holding abbreviations such as AL end in CD to indicate they are a code for some meaning. E.g. AL is a state code for the state name Alabama.
- DT: Dates are the format 'YYYY-MM-DD' such as '2999-12-31'
- ID: These are integer fields always and hold an identification number such as IMM_ID being the identification number for an immigration case.
- NM: These fields are descriptive names that don't need interpretation, such as Alabama being a state name.
- YR: An integer-field describing the year.
- NO: Numerical fields much like ID but where the number might not be sufficiently unique to mark an ID
- AMT: Numerical field which holds amounts typically in a decimal form such as a bank balance amt.

In general, the field names are abbreviated to three or four-letter words ending in one of the four suffixes above unless it is clear what the name holds such as 'AGE' where it seems excessive to say 'AGE_YR'.

**Immigration data**

The main tables are a snowflake set of tables with an immigration fact table in the center surrounded by immigration dimension tables. All immigration data have code fields ("\_CD") that refer to some abbreviation or ID that can be decoded. To decode these, a set of CODE-tables have been set up that link to the immigration tables.

**Supplementary data**

In addition to the immigration tables we have tables that don't directly link to the Immigration data set. These data sets are temperature, demographics and airports data. Each have been normalised to the most reasonable degree. See the graph underneath to get an idea of the entities' relationships.

A difficult decision was whether or not to extract code fields to separate tables or translate them directly in the table. For this data model it was decided that the code-fields should reside in separate tables, which could eventually all be combined to one large code-table holding a field for domain, a field for code value and a field for the corresponding meaning of the code value.

**Notes on relationships**

Note that although there are tables to decrypt most code-fields, these tables don't necessarily pair well due to a lack of data. E.g. temperature data and airport data both have longitudes and latitudes and should thus be able to pair. In practice, since temperatures aren't generally measured at airports the relationships are impaired.

## Immigration Data
This data set holds data relating to immigration to the US. The focal field is the ID (cicid) for each immigration case to the US. In addition, the table holds information on the person related to the case, how and where this person arrived to the US, which date the person arrived respectively was granted admission, and if this person left again.

This table will be split into four tables consisting of a fact table and three dimension tables describing the person dimension, the arrival dimension and the visa dimension. Togerher with a description file, we will further extend each of these tables with translation of various abbrevations (codes) into human readable values.

### Fact table
The fact table holds facts about admission to the US as well as departure from the country in addition to method travelled to the country. Through the IMM_ID (immigration ID), we can learn about the person immigrating, the arrival (assuming the person flew in), and the VISA.

### Dimension tables

#### Visa Dimension table
Describes conditions for VISA application.

#### Person Dimension table
Describes the immigrant arriving into the US.

#### Arrival Dimension table
Describes the arrival information into the US assuming immigrant arrived by air.

### Temperature data set
The temperature data provides information on average temperature measurements in cities around the world from November 1st, 1743 and onwards. 

The data set will be split according to two fact types, (1) being the data and temperature, and (2) being the city and it's location in latitude and longitude. The split allows for a normalisation such that city information isn't repeated for every single temperate observation.

### Demographics data set
This table holds information on city populations with respect to age, male/female population, veteran and foreign-born population, and race statistics. The race statistics are registered in a long-format, such that all other statistics are repeated for each race that the city has measurements for. 

The data set structure calls for a normalisation which requires at least two tables. Here, the split goes into three tables:
1. A table not holding race statistics
2. A table holding race statistics, race being abbreviated into codes
3. A table holding abbreviated race codes and the race names associated with each code
This separation allows for normalisation of the table.

The table connects to immigration data through the state codes.

### Airport data
This data set holds information airports regarding their size, location and elevation etc.

The data set connects to the temperature data set through latitude and longitude values (although generally we don't have measurements for airport locations), and additionally we can connect to the immigration data set through IATA_ARPT_CD on visapost. This can only be done under the assumption that the visapost, which is a code for the department that has issued the visa to an immigrant, is done at an airport, and that the code in fact is an IATA_ARPT_CD.

There are no obvious ways to improve this data, although it can be argued that some fields are redundant. Without more business knowledge it is difficult to know which ones, and hence I keep the data.

Generally, ident seems to be similar to gps_code, iata_code and local_code, but there are exceptions everywhere between these columns.

### Additional Code tables
An additional set of tables can be extracted from a text file. Udacity mentors helped in developing the code. These tables mainly provide translation of abbreviations or code into human readable information. No further comment will be provided. An additional table will be provided by manually inserting values that are taken from various Google searches.

# Implementation
The setup requires an IAM user in AWS that allows to store the data into an S3 cluster after transformations from their local files. Additionally, the program is written in pyspark to allow for big data manipulation. All transformations of data ultimately lead to creating the tables for the star schema and writing parquet files to the S3 cluster. The notebook provides a method to further run a Redshift cluster where data can be loaded to and computations can be made. We will not cover the use of Airflow.

# Further comments
Please see the jupyter notebook for a thorough run-through of all data.
