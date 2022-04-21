/*
Aggregation pipeline to compress Actor1, Actor2, and Action fields into it's own subdocument.
*/

// Select the database to use.
use('GDELT2');

// Build an aggregation pipeline to compress Actor1, Actor2, and Action fields into it's own subdocument.
// Map lat/long to GeoJSON coordinates.

const GDELTAggregation = [
    {
        $addFields: {
            Actor1Geo: {
                "type": "Point",
                "coordinates": [
                    {$convert: {input: "$Actor1Geo_Long", to: "double", onError: 0.00, onNull: 0.00}},
                    {$convert: {input: "$Actor1Geo_Lat", to: "double", onError: 0.00, onNull: 0.00}}
                ]
            },
            Actor2Geo: {
                "type": "Point",
                "coordinates": [
                    {$convert: {input: "$Actor2Geo_Long", to: "double", onError: 0.00, onNull: 0.00}},
                    {$convert: {input: "$Actor2Geo_Lat", to: "double", onError: 0.00, onNull: 0.00}}
                ]
            },
            ActionGeo: {
                "type": "Point",
                "coordinates": [
                    {$convert: {input: "$ActionGeo_Long", to: "double", onError: 0.00, onNull: 0.00}},
                    {$convert: {input: "$ActionGeo_Lat", to: "double", onError: 0.00, onNull: 0.00}}
                ]
            }
        }
    },
    {
        $addFields: {
            Actor1: {
                Name: '$Actor1Name',
                "Code": '$Actor1Code',
                CountryCode: '$Actor1CountryCode',
                KnownGroupCode: '$Actor1KnownGroupCode',
                EthnicCode: '$Actor1EthnicCode',
                Religion1Code: '$Actor1Religion1Code',
                Religion2Code: '$Actor1Religion2Code',
                Type1Code: '$Actor1Type1Code',
                Type2Code: '$Actor1Type2Code',
                Type3Code: '$Actor1Type3Code',
                Geo: "$Actor1Geo",
                Geo_Type: "$Actor1Geo_Type",
                Geo_Fullname: "$Actor1Geo_Fullname",
                Geo_CountryCode: "$Actor1Geo_CountryCode",
                Geo_ADM1Code: "$Actor1Geo_ADM1Code",
                Geo_ADM2Code: "$Actor1Geo_ADM2Code",
                Geo_FeatureID: "$Actor1Geo_FeatureID"
            },
            Actor2: {
                Name: '$Actor2Name',
                "Code": '$Actor2Code',
                CountryCode: '$Actor2CountryCode',
                KnownGroupCode: '$Actor2KnownGroupCode',
                EthnicCode: '$Actor2EthnicCode',
                Religion1Code: '$Actor2Religion1Code',
                Religion2Code: '$Actor2Religion2Code',
                Type1Code: '$Actor2Type1Code',
                Type2Code: '$Actor2Type2Code',
                Type3Code: '$Actor2Type3Code',
                Geo: "$Actor2Geo",
                Geo_Type: "$Actor2Geo_Type",
                Geo_Fullname: "$Actor2Geo_Fullname",
                Geo_CountryCode: "$Actor2Geo_CountryCode",
                Geo_ADM1Code: "$Actor2Geo_ADM1Code",
                Geo_ADM2Code: "$Actor2Geo_ADM2Code",
                Geo_FeatureID: "$Actor2Geo_FeatureID"
            },
            Action: {
                "Geo": "$ActionGeo",
                "Geo_Type": "$ActionGeo_Type",
                "Geo_Fullname": "$ActionGeo_Fullname",
                "Geo_CountryCode": "$ActionGeo_CountryCode",
                "Geo_ADM1Code": "$ActionGeo_ADM1Code",
                "Geo_ADM2Code": "$ActionGeo_ADM2Code",
                "Geo_FeatureID": "$ActionGeo_FeatureID"
            },
        }
    },
    {
        $unset: [
            "Actor1Name",
            "Actor1Code",
            "Actor1CountryCode",
            "Actor1KnownGroupCode",
            "Actor1EthnicCode",
            "Actor1Religion1Code",
            "Actor1Religion2Code",
            "Actor1Type1Code",
            "Actor1Type2Code",
            "Actor1Type3Code",
            "Actor1Geo",
            "Actor1Geo_Type",
            "Actor1Geo_Fullname",
            "Actor1Geo_CountryCode",
            "Actor1Geo_ADM1Code",
            "Actor1Geo_ADM2Code",
            "Actor1Geo_FeatureID",
            "Actor2Code",
            "Actor2Name",
            "Actor2CountryCode",
            "Actor2KnownGroupCode",
            "Actor2EthnicCode",
            "Actor2Religion1Code",
            "Actor2Religion2Code",
            "Actor2Type1Code",
            "Actor2Type2Code",
            "Actor2Type3Code",
            "Actor2Geo",
            "Actor2Geo_Type",
            "Actor2Geo_Fullname",
            "Actor2Geo_CountryCode",
            "Actor2Geo_ADM1Code",
            "Actor2Geo_ADM2Code",
            "Actor2Geo_FeatureID",
            "ActionGeo",
            "ActionGeo_Type",
            "ActionGeo_Fullname",
            "ActionGeo_CountryCode",
            "ActionGeo_ADM1Code",
            "ActionGeo_ADM2Code",
            "ActionGeo_FeatureID",
            "ActionGeo_Lat",
            "ActionGeo_Long",
            "Actor1Geo_Lat",
            "Actor1Geo_Long",
            "Actor2Geo_Lat",
            "Actor2Geo_Long"
        ]
    },
    {
        $out: "events"
    }
];

db.eventscsv.aggregate(GDELTAggregation);
