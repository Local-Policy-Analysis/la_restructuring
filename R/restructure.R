library(dplyr)
library(readr)
library(readxl)

restructure <- function(df, from_year, to_year, by = c("ons_code" = str_c("ons_code_",from_year))){
    loc <- "https://raw.githubusercontent.com/Local-Policy-Analysis/la_restructuring/main/bin/la_structure.tsv"
    stopifnot(from_year < to_year)

    stopifnot(
        typeof(from_year <- toString(from_year)) == "character",
        typeof(to_year <- toString(to_year)) == "character"
    )


    dfLookup <- read_tsv(url(loc)) |>
        select(STATUS, contains(from_year), contains(to_year))

    fails <- anti_join(df, dfLookup, by = by)

    if(nrow(fails) > 0){
        warning(str_c(nrow(fails), " ONS codes failed to match"))
    }

    return(left_join(df, dfLookup, by = by) |> 
    select(ons_code, contains(from_year), contains(to_year)))
}

df <- read_excel("./to_restructure.xlsx")
df <- restructure(df, 2013, 2023)

write_csv(df, "test.csv")
