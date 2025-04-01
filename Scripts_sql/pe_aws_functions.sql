SET FOREIGN_KEY_CHECKS = 0;

SET GLOBAL log_bin_trust_function_creators = 1;
-- ----------------------------------------------------------------------------
-- Routine PE_AWS.claimedBlogger
-- ----------------------------------------------------------------------------

DELIMITER $$

DELIMITER $$
USE `PE_AWS`$$
CREATE FUNCTION `claimedBlogger`(blogger_idX int) RETURNS varchar(500) CHARSET latin1
    DETERMINISTIC
BEGIN
        DECLARE claimed VARCHAR(500);
        SET claimed=(
					select 
					if (length(d.user_id)>0,"YES","NO") as claimed

					from bloggers as a
					left outer join crm_companies as b on b.blogger_id=a.id
					left outer join crm_contacts as c on c.company_id=b.id
					left outer join users as d on c.pe_record=d.user_id
					where a.id=blogger_idX  and c.permission like '%Accessible%'
                    group by a.id);       
RETURN claimed;

END$$

DELIMITER ;

-- ----------------------------------------------------------------------------
-- Routine PE_AWS.claimedBusiness
-- ----------------------------------------------------------------------------
DELIMITER $$

DELIMITER $$
USE `PE_AWS`$$
CREATE FUNCTION `claimedBusiness`(profile_idX int) RETURNS varchar(500) CHARSET latin1
    DETERMINISTIC
BEGIN
        DECLARE claimed VARCHAR(500);
        SET claimed=(
					select 
					if (length(d.user_id)>0,"YES","NO") as claimed

					from businessprofiles as a
					left outer join crm_companies as b on b.profile_id=a.id
					left outer join crm_contacts as c on c.company_id=b.id
					left outer join users as d on c.pe_record=d.user_id
					where a.id=profile_idX  and c.permission like '%Accessible%'
                    group by a.id);       
RETURN claimed;

END$$

DELIMITER ;

-- ----------------------------------------------------------------------------
-- Routine PE_AWS.commPrice
-- ----------------------------------------------------------------------------
DELIMITER $$

DELIMITER $$
USE `PE_AWS`$$
CREATE FUNCTION `commPrice`(productIDx int) RETURNS varchar(500) CHARSET latin1
    DETERMINISTIC
BEGIN

   DECLARE price VARCHAR(500);
        SET price=(
					select 
					If ( length(min(f.basic_price))>0, min(f.basic_price), 
                    If ( length(min(c.basic_price))>0, min(c.basic_price), 
                    if ( length(min(d.basic_price))>0, concat_ws('',min(round(d.basic_price)),' (',d.amount_time,' ',d.units_time,') '),
					if ( length(min(e.basic_price))>0, concat_ws('',min(round(e.basic_price)),' (',e.room_type,') '),
                    '')))) as Price
					
                    from businessprofiles_products as a                  
					left outer join businessprofiles_productsprices as c on c.product_id=a.id and  c.pricing_scheme in ('Standard','Adults','Participants') and (quantity='1' or quantity=a.min_quantity)  and  (c.pricing_type!='Discount' or c.pricing_type is null)
					left outer join businessprofiles_productsprices as d on d.product_id=a.id and (d.pricing_scheme='Time' or d.pricing_scheme='Rental') and  (d.pricing_type!='Discount' or d.pricing_type is null)
                    left outer join businessprofiles_productsprices as e on e.product_id=a.id and (e.pricing_scheme='Room')
                    Left outer join businessprofiles_productsprices as f on f.product_id=a.id and (f.pricing_scheme='API')
                    
                    where a.id=productIDx
                    group by a.id);
                    
                    
RETURN price;

END$$

DELIMITER ;

-- ----------------------------------------------------------------------------
-- Routine PE_AWS.commRate
-- ----------------------------------------------------------------------------
DELIMITER $$

DELIMITER $$
USE `PE_AWS`$$
CREATE FUNCTION `commRate`(productIDx int) RETURNS varchar(500) CHARSET latin1
    DETERMINISTIC
BEGIN

   DECLARE commRate VARCHAR(500);
        SET commRate=(
					select 
                    
                      case  when e.comm_active=1 then
							 if( length(a.comm_1) > 0 , a.comm_1, if ( length(e.comm_1) > 1, e.comm_1, 'N/A')) 
                       when e.comm_active=2 then
                             if( length(a.comm_2) > 0 , a.comm_2, if ( length(e.comm_2) > 1, e.comm_2, 'N/A')) 
						end as comm1
                    				
                                    
                    
                    
                    
					from businessprofiles_products as a                  
					left outer join businessprofiles_productsprices as c on c.product_id=a.id and c.pricing_scheme='Standard' and (quantity='1' or quantity=a.min_quantity)
					left outer join businessprofiles_productsprices as d on d.product_id=a.id and (d.pricing_scheme='Time' or d.pricing_scheme='Rental') 
					left outer join businessprofiles as e on a.profile_id=e.id
                   where a.id=productIDx
                    group by a.id);
                    
                    
RETURN commRate;


END$$

DELIMITER ;

-- ----------------------------------------------------------------------------
-- Routine PE_AWS.saParent
-- ----------------------------------------------------------------------------
DELIMITER $$

DELIMITER $$
USE `PE_AWS`$$
CREATE FUNCTION `saParent`(idX int) RETURNS varchar(500) CHARSET latin1
BEGIN


        DECLARE tags VARCHAR(500);
        SET tags=(
				  SELECT group_concat( distinct(  
						if (t.parent_id=2,t.tag_name,tp.tag_name)

						)) as tags
					 FROM sightsattractions as x
					join sightsattractions_totags as xy on xy.offering_id=x.id
					left outer join tags as t on t.id=xy.tag_id 
					left outer join tags as tp on t.parent_id=tp.id    and tp.parent_id=2
					where x.id=idX
					group by x.id  );       
RETURN tags;

END$$

DELIMITER ;


-- ----------------------------------------------------------------------------
-- Routine PE_AWS.userOwns
-- ----------------------------------------------------------------------------
DELIMITER $$

DELIMITER $$
USE `PE_AWS`$$
CREATE FUNCTION `userOwns`(user_idX int) RETURNS varchar(2000) CHARSET latin1
    DETERMINISTIC
BEGIN
        DECLARE ownership VARCHAR(2000);
        SET ownership=(SELECT 
				group_concat( CASE WHEN LENGTH(d.name) > 0 and c.trigger_invoices=1 THEN concat_ws('','Invoice',';;',d.name,';;',d.id,';;',a.role,';;',a.permission)
								WHEN LENGTH(d.name) > 0 THEN concat_ws('','Business',';;',d.name,';;',d.id,';;',a.role,';;',a.permission)
								 WHEN c.type="Travel Agency" then concat_ws('','Travel Agency',';;',c.name,';;',c.id,';;',a.role,';;',a.permission)
                                 WHEN c.type="Host Agency / Franchisor" then concat_ws('','Travel Agency',';;',c.name,';;',c.id,';;',a.role,';;',a.permission)
								 WHEN c.campaign="Partnership" then concat_ws('','Partner',';;',c.name,';;',c.id,';;',a.role,';;',a.permission)
								 when c.campaign="Expansion" then concat_ws('','Business',';;','',';;','',';;','',';;',a.permission)
                                 WHEN LENGTH(e.blog_name)>0 THEN concat_ws('','Blog',';;',e.blog_name,';;',e.id,';;',a.role,';;',a.permission)
                              	WHEN b.user_type in (1,2,3,4) THEN concat_ws('','Internal',';;',b.first_name,';;',b.user_id,';;','',';;','')   
								 else concat_ws('','Traveler',';;','',';;','',';;','')   END        
				 SEPARATOR "~~~") as ownership
			FROM users as b
            left outer join crm_contacts as a on a.pe_record=b.user_id 
			left outer join crm_companies as c on a.company_id=c.id
			left outer join businessprofiles as d on c.profile_id=d.id
			left outer join bloggers as e on c.blogger_id=e.id
			WHERE b.user_id=user_idX );        
RETURN ownership;

END$$

DELIMITER ;

SET FOREIGN_KEY_CHECKS = 1;

#use pe_aws;
#drop table helpdesk_communication;