# Constants
DROP_IF = "DROP TABLE IF EXISTS "
CREATE_IF = "CREATE TABLE IF NOT EXISTS "

create_staging_immigration_table = CREATE_IF + """
    staging_immigration 
    (
        cicid                         numeric(18,2),
        i94yr                         numeric(18,2),
        i94mon                        numeric(18,2),
        i94cit                        numeric(18,2),
        i94res                        numeric(18,2),
        i94port                       varchar(256) ,
        arrdate                       numeric(18,2),
        i94mode                       numeric(18,2),
        i94addr                       varchar(256) ,
        depdate                       numeric(18,2),
        i94bir                        numeric(18,2),
        i94visa                       numeric(18,2),
        count                         numeric(18,2),
        dtadfile                      varchar(256) ,
        visapost                      varchar(256) ,
        occup                         varchar(256) ,
        entdepa                       varchar(256) ,
        entdepd                       varchar(256) ,
        entdepu                       varchar(256) ,
        matflag                       varchar(256) ,
        biryear                       numeric(18,2),
        dtaddto                       varchar(256) ,
        gender                        varchar(256) ,
        insnum                        varchar(256) ,
        airline                       varchar(256) ,
        admnum                        numeric(18,2),
        fltno                         varchar(256) ,
        visatype                      varchar(256) 
    )"""

create_staging_temperature_table = CREATE_IF + """
    staging_temperature 
    (
        dt                            date         ,
        AverageTemperature            numeric(18,0),
        AverageTemperatureUncertainty numeric(18,0),
        City                          varchar(256) ,
        Country                       varchar(256) ,
        Latitude                      varchar(256) ,
        Longitude                     varchar(256)
    )"""

create_staging_demographics_table = CREATE_IF + """
    staging_demographics 
    (
        City                          varchar(256) ,
        State                         varchar(256) ,
        Median_Age                    numeric(18,0),
        Male_population               int4         ,
        Female_population             int4         ,
        Total_Population              int4         ,
        Number_of_Veterans            int4         ,
        Foreign_born                  int4         ,
        Average_Household_Size        numeric(18,0),
        State_Code                    varchar(256) ,
        Race                          varchar(256) ,
        Count                         int4
    )"""

create_staging_airports_table = CREATE_IF + """
    staging_airports 
    (
        ident                         varchar(256) ,
        type                          varchar(256) ,
        name                          varchar(256) ,
        elevation_ft                  int4         ,
        continent                     varchar(256) ,
        iso_country                   varchar(256) ,
        iso_region                    varchar(256) ,
        municipality                  varchar(256) ,
        gps_code                      varchar(256) ,
        iata_code                     varchar(256) ,
        local_code                    varchar(256) ,
        coordinates                   varchar(256)
    )
"""



create_staging_table_queries = [
    create_staging_immigration_table,
    create_staging_temperature_table, 
    create_staging_demographics_table, 
    create_staging_airports_table
]


# IMMIGRATION DATA
create_imm_fct = CREATE_IF + """
    IMM_FCT 
    (
        IMM_ID                 INTEGER     PRIMARY KEY,
        ADM_CD                 CHAR(1)     ,
        ADM_MTD_CD             INTEGER     ,
        ADM_NO                 INTEGER     ,
        ADM_DT                 DATE        ,
        DEP_CD                 CHAR(1)     ,
        DEP_DT                 DATE        ,
        ADM_UPD_CD             CHAR(1)
    )"""

create_imm_psn_dim = CREATE_IF + """
    IMM_DIM_PSN 
    (
        IMM_ID                 INTEGER     PRIMARY KEY,
        INS_ID                 INTEGER     ,
        BRTH_YR                INTEGER     ,
        AGE                    INTEGER     ,
        OCC_CD                 CHAR(3)     ,
        GNDR_CD                CHAR(1)     ,
        CTY_OF_RSDN_ID         INTEGER     ,
        CTY_OF_CTZ_ID          INTEGER     ,
        ADR_RGN_CD             CHAR(2)
    )"""

create_imm_visa_dim = CREATE_IF + """
    IMM_DIM_VISA
    (
        IMM_ID                 INTEGER     PRIMARY KEY,
        VISA_TP_CD             CHAR(2)     ,
        VISA_RSN_CD            INTEGER     ,
        VISA_ISSU_DEP_CD       CHAR(3)
    )"""

create_imm_arpt_dim = CREATE_IF + """
    IMM_DIM_ARPT 
    (
        IMM_ID                 INTEGER     PRIMARY KEY,
        ARPT_CD                CHAR(3)     ,
        ARLN_CD                CHAR(2)     ,
        FLGT_CD                CHAR(5)     ,
        ARR_DT                 DATE
    )"""

create_imm_tables = [
    create_imm_fct,
    create_imm_psn_dim,
    create_imm_visa_dim,
    create_imm_arpt_dim
]

# CODE TABLES
create_cd_adm_mtd = CREATE_IF + """
    CD_ADM_MTD 
    (
        ADM_MTD_CD             CHAR(1)     PRIMARY KEY,
        ADM_MTD_NM             VARCHAR(100)
    )"""

create_cd_adm_st = CREATE_IF + """
    CD_ADM_ST
    (
        ADM_ST_CD              CHAR(1)     PRIMARY KEY,
        ADM_ST_NM              VARCHAR(100)
    )
"""

create_cd_arpt = CREATE_IF + """
    CD_ARPT 
    (
        ARPT_CD                CHAR(3)     PRIMARY KEY,
        ARPT_NM                VARCHAR(100),
        ARPT_STT_CD            CHAR(2)
    )"""

create_cd_cty = CREATE_IF + """
    CD_CTY 
    (
        CTY_CD                 CHAR(3)     PRIMARY KEY,
        CTY_NM                 VARCHAR(100)
    )"""

create_cd_dep = CREATE_IF + """
    CD_DEP
    (
        DEP_CD                 CHAR(1)     PRIMARY KEY,
        DEP_NM                 VARCHAR(150)
    )"""

create_cd_rgn = CREATE_IF + """
    CD_RGN 
    (
        RGN_CD                 CHAR(2)     PRIMARY KEY,
        RGN_NM                 VARCHAR(100)
    )"""

create_cd_visa_rsn = CREATE_IF + """
    CD_VISA_RSN
    (
        VISA_RSN_CD            INTEGER     PRIMARY KEY,
        VISA_RSN_NM            VARCHAR(100)
    )"""


create_cd_tables = [
    create_cd_adm_mtd,
    create_cd_adm_st,
    create_cd_arpt,
    create_cd_cty,
    create_cd_dep,
    create_rgn_cd,
    create_visa_rsn_cd
]

# TEMPERATURE TABLES
create_temp_fct = CREATE_IF + """
    TEMP_FCT 
    (
        TEMP_CITY_ID           INTEGER     PRIMARY KEY,
        TEMP_MSR_DT            DATE        ,
        TEMP_AVG_VAL           DECIMAL(5,3),
        TEMP_SD_VAL            DECIMAL(5,3)
    )"""

create_temp_city_dim = CREATE_IF + """
    TEMP_DIM_CITY 
    (
        TEMP_CITY_ID           INTEGER     PRIMARY KEY,
        CITY_NM                VARCHAR(255),
        CTY_NM                 VARCHAR(255),
        LAT_VAL                DECIMAL(4,2),
        LONG_VAL               DECIMAL(5,2)
    )"""

create_temp_tables = [
    create_temp_fct,
    create_temp_city_dim
]

# AIRPORT TABLES
create_arpt_fct = CREATE_IF + """
    ARPT_FCT
    (
        ARPT_ID                CHAR(4)     PRIMARY KEY,
        ARPT_TP                VARCHAR(20) ,
        ARPT_NM                VARCHAR(255),
        ELEV_FT                DECIMAL(9,2),
        CONT_CD                CHAR(2)     ,
        ISO_CTY_CD             CHAR(2)     ,
        ISO_RGN_CD             CHAR(7)     ,
        MUNI_NM                VARCHAR(255),
        GPS_CD                 CHAR(4)     ,
        IATA_ARPT_CD           CHAR(3)     ,
        LCL_ARPT_CD            CHAR(3)     ,
        LAT_VAL                DECIMAL(4,2),
        LONG_VAL               DECIMAL(5,2)
    )"""

create_arpt_tables = [create_arpt_fct]


# DEMOGRAPHICS TABLES
create_demo_fct = CREATE_IF + """
    DEMO_FCT 
    (
        DEMO_CITY_ID           INTEGER     PRIMARY KEY,
        RGN_CD                 CHAR(2)     ,
        RGN_NM                 VARCHAR(255),
        CITY_NM                VARCHAR(255),
        MED_AGE                DECIMAL(4,1),
        POP_TOT_AMT            INTEGER     ,
        POP_MLE_AMT            INTEGER     ,
        POP_FMLE_AMT           INTEGER     ,
        POP_VET_AMT            INTEGER     ,
        POP_FGN_AMT            INTEGER     ,
        AVG_HH_SZ              DECIMAL(4,2)
    )"""

create_demo_race_fct = CREATE_IF + """
    DEMO_FCT_RACE 
    (
        DEMO_CITY_ID           INTEGER     PRIMARY KEY,
        RACE_TP_CD             CHAR(4)     ,
        POP_RACE_AMT           INTEGER
    )"""

create_demo_race_cd = CREATE_IF + """
    CD_RACE_TP
    (
        RACE_TP_CD             CHAR(4)     PRIMARY KEY, 
        RACE_TP_NM             VARCHAR(50)
    )"""

create_demo_tables = [
    create_demo_fct,
    create_demo_race_fct,
    create_demo_race_cd
]

create_data_model_tables = [
    *create_imm_tables,
    *create_temp_tables,
    *create_arpt_tables,
    *create_demo_tables, 
    *create_cd_tables
]
