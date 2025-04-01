use PE_AWS;

#drop database PRD_PE_AWS;
#drop database pe_aws;

select count(*) from PE_AWS.audittrail; # 47303576
select count(*) from PRD_PE_AWS.audittrail; # 47303576 # ask wiki

select count(*) from PE_AWS.bloggers; # 777
select count(*) from PRD_PE_AWS.bloggers; # 777

select count(*) from PE_AWS.bookings; # 692575
select count(*) from PRD_PE_AWS.bookings; # 692575 #fallo

select count(*) from PE_AWS.bookings_discounts; # 1353 
select count(*) from PRD_PE_AWS.bookings_discounts; # 1353 

select count(*) from PE_AWS.bookings_payments; # 277013
select count(*) from PRD_PE_AWS.bookings_payments; # 277013

select count(*) from PE_AWS.businessprofiles; # 4773
select count(*) from PRD_PE_AWS.businessprofiles; # 4773

select count(*) from PE_AWS.businessprofiles_awardsachieve; # 14
select count(*) from PRD_PE_AWS.businessprofiles_awardsachieve; # 14

select count(*) from PE_AWS.businessprofiles_bios; # 685
select count(*) from PRD_PE_AWS.businessprofiles_bios; # 685

select count(*) from PE_AWS.businessprofiles_licensecert; # 177
select count(*) from PRD_PE_AWS.businessprofiles_licensecert; # 177

select count(*) from PE_AWS.businessprofiles_paymentoptions; # 3664
select count(*) from PRD_PE_AWS.businessprofiles_paymentoptions; # 3664

select count(*) from PE_AWS.businessprofiles_products; # 77823
select count(*) from PRD_PE_AWS.businessprofiles_products; # 77823 #ask wiki

select count(*) from PE_AWS.businessprofiles_productsactivities; # 297803
select count(*) from PRD_PE_AWS.businessprofiles_productsactivities; # 297803 # ask wiki

select count(*) from PE_AWS.businessprofiles_productsactivitiestags; # 75611
select count(*) from PRD_PE_AWS.businessprofiles_productsactivitiestags; # 75611

select count(*) from PE_AWS.businessprofiles_productsaddons; # 24109
select count(*) from PRD_PE_AWS.businessprofiles_productsaddons; # 24109

select count(*) from PE_AWS.businessprofiles_productsavailability; #54641
select count(*) from PRD_PE_AWS.businessprofiles_productsavailability; #54641 

select count(*) from PE_AWS.businessprofiles_productscatchment; #25749
select count(*) from PRD_PE_AWS.businessprofiles_productscatchment; #25749

select count(*) from PE_AWS.businessprofiles_productslanguages;#55799
select count(*) from PRD_PE_AWS.businessprofiles_productslanguages;#55799 # ASK MANUEL

select count(*) from PE_AWS.businessprofiles_productsprices;#191527
select count(*) from PRD_PE_AWS.businessprofiles_productsprices;#191527 # fallo

select count(*) from PE_AWS.crm_companies;#36102
select count(*) from PRD_PE_AWS.crm_companies;#36102

select count(*) from PE_AWS.crm_contacts; #62294
select count(*) from PRD_PE_AWS.crm_contacts; #62294 # ASK WIKI # fallo

select count(*) from PE_AWS.crm_interactions; #47101
select count(*) from PRD_PE_AWS.crm_interactions; #47101 # fallo

select count(*) from PE_AWS.cruiseship_schedules; #57357
select count(*) from PRD_PE_AWS.cruiseship_schedules; #57357

select count(*) from PE_AWS.cruiseship_schedules_ports; # 484402
select count(*) from PRD_PE_AWS.cruiseship_schedules_ports; # 484402

select count(*) from PE_AWS.currencies; # 49
select count(*) from PRD_PE_AWS.currencies; # 49

select count(*) from PE_AWS.currencies_exchange_rates; #241
select count(*) from PRD_PE_AWS.currencies_exchange_rates; #241

select count(*) from PE_AWS.emails; #106077
select count(*) from PRD_PE_AWS.emails; #106077 # ASK WIKI fallo

select count(*) from PE_AWS.emails_unsubscribe;#264
select count(*) from PRD_PE_AWS.emails_unsubscribe;#264 # fallo

select count(*) from PE_AWS.faq; #845
select count(*) from PRD_PE_AWS.faq; #845

select count(*) from PE_AWS.fielddefinitions; # 139
select count(*) from PRD_PE_AWS.fielddefinitions; # 139 # fallo

select count(*) from PE_AWS.geography_countries; #178
select count(*) from PRD_PE_AWS.geography_countries; #178

select count(*) from PE_AWS.geography_countriescustomfields; #814
select count(*) from PRD_PE_AWS.geography_countriescustomfields; #814

select count(*) from PE_AWS.geography_regions; # 1931
select count(*) from PRD_PE_AWS.geography_regions; # 1931

select count(*) from PE_AWS.geography_regionstypes; #18
select count(*) from PRD_PE_AWS.geography_regionstypes; #18

select count(*) from PE_AWS.geography_subcontinents; #19
select count(*) from PRD_PE_AWS.geography_subcontinents; #19

select count(*) from PE_AWS.geography_towns; # 5474
select count(*) from PRD_PE_AWS.geography_towns; # 5474

select count(*) from PE_AWS.helpdesk; #374747 # 
select count(*) from PRD_PE_AWS.helpdesk; #374747 # ask wiki

select count(*) from PE_AWS.helpdesk_communication; #1707741
select count(*) from PRD_PE_AWS.helpdesk_communication; #1707741 # ask wiki

select count(*) from PE_AWS.info;#14158332
select count(*) from PRD_PE_AWS.info;#14158332 # ask wiki

select count(*) from PE_AWS.info_avail_check; #0
select count(*) from PRD_PE_AWS.info_avail_check; #0

select count(*) from PE_AWS.info_chat_check; #0
select count(*) from PRD_PE_AWS.info_chat_check; #0

select count(*) from PE_AWS.languages; #52
select count(*) from PRD_PE_AWS.languages; #52

select count(*) from PE_AWS.photos; # 332065 
select count(*) from PRD_PE_AWS.photos; # 332065 # ask wiki

select count(*) from PE_AWS.places; #138496
select count(*) from PRD_PE_AWS.places; #138496 ask wiki

select count(*) from PE_AWS.places_products; # 823808
select count(*) from PRD_PE_AWS.places_products; # 823808 ask wiki

select count(*) from PE_AWS.reviews; # 10108
select count(*) from PRD_PE_AWS.reviews; # 10108 # ask wiki

select count(*) from PE_AWS.short_links;# 558759
select count(*) from PRD_PE_AWS.short_links;# 558759 # ask wiki

select count(*) from PE_AWS.sightsattractions; # 16606
select count(*) from PRD_PE_AWS.sightsattractions; # 16606 #ask wiki

select count(*) from PE_AWS.sightsattractions_customfields; # 16
select count(*) from PRD_PE_AWS.sightsattractions_customfields; # 16

select count(*) from PE_AWS.sightsattractions_openinghours; #979
select count(*) from PRD_PE_AWS.sightsattractions_openinghours; #979

select count(*) from PE_AWS.sightsattractions_totags; # 18165
select count(*) from PRD_PE_AWS.sightsattractions_totags; # 18165

select count(*) from PE_AWS.tag_types; # 7
select count(*) from PRD_PE_AWS.tag_types; # 7

select count(*) from PE_AWS.tags; #1054
select count(*) from PRD_PE_AWS.tags; #1054 # fallo

select count(*) from PE_AWS.tags_alternate_names; #131
select count(*) from PRD_PE_AWS.tags_alternate_names; #131

select count(*) from PE_AWS.transportation; # 14100
select count(*) from PRD_PE_AWS.transportation; # 14100 # ask wiki

select count(*) from PE_AWS.trips; # 11
select count(*) from PRD_PE_AWS.trips; # 11

select count(*) from PE_AWS.trips_goodfor; #68
select count(*) from PRD_PE_AWS.trips_goodfor; #68

select count(*) from PE_AWS.trips_stops; #132
select count(*) from PRD_PE_AWS.trips_stops; #132

select count(*) from PE_AWS.users; #65017
select count(*) from PRD_PE_AWS.users; #65017 # ask wiki

select count(*) from PE_AWS.users_apipermissioning; #4825
select count(*) from PRD_PE_AWS.users_apipermissioning; #4825

select count(*) from PE_AWS.users_permissioning;# 1074
select count(*) from PRD_PE_AWS.users_permissioning;# 1074

select count(*) from PE_AWS.users_permissioningpages; #68
select count(*) from PRD_PE_AWS.users_permissioningpages; #68

select count(*) from PE_AWS.users_types; #5
select count(*) from PRD_PE_AWS.users_types; #5

select count(*) from PE_AWS.users_wishlist; #216956
select count(*) from PRD_PE_AWS.users_wishlist; #216956 #ask wiki

select count(*) from PE_AWS.videos; # 1533
select count(*) from PRD_PE_AWS.videos; # 1533

/* len of each table*/
SELECT table_name, table_rows
FROM information_schema.tables
WHERE table_schema = 'PE_AWS';

/* number of tables of each type*/
SELECT table_name, COUNT(*) as row_count
FROM information_schema.tables
WHERE table_schema = 'PE_AWS'
GROUP BY table_name;

