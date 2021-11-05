-- ----------------------------------------------------------------
--  FUNCTION fn_hrm_salary_processing
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_hrm_salary_processing (
   IN      p_branch_code   INTEGER,
   IN      p_dept_id       CHARACTER,
   IN      p_month_year    CHARACTER,
   IN      p_app_user_id   CHARACTER,
       OUT o_status        CHARACTER,
       OUT o_errm          CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_message    VARCHAR;
   w_status     VARCHAR;
   w_errm       VARCHAR;
   v_time       TIMESTAMP (6) := CURRENT_TIMESTAMP;
   w_sql_stat   TEXT := '';
BEGIN
   DELETE FROM HRM_SALARY_SHEET
         WHERE MONTH_YEAR = P_MONTH_YEAR;

   DELETE FROM sales_sales_commission
         WHERE SALES_MONTH = P_MONTH_YEAR;

   INSERT INTO sales_sales_commission (EMPLOYEE_ID,
                                       SALES_MONTH,
                                       SALES_QUANTITY,
                                       TOTAL_PRICE)
        SELECT EMPLOYEE_ID,
               SALES_MONTH,
               SUM (SALES_QUANTITY) SALES_QUANTITY,
               SUM (SALES_QUANTITY * TOTAL_PRICE) TOTAL_PRICE
          FROM (SELECT E.EMPLOYEE_ID,
                       TO_CHAR (INVOICE_DATE, 'MON-YYYY')
                          SALES_MONTH,
                       COALESCE (QUANTITY) - COALESCE (D.RETURNED_QUANTITY)
                          SALES_QUANTITY,
                       COALESCE (TOTAL_PRICE)
                          TOTAL_PRICE
                  FROM SALES_SALES_DETAILS D,
                       SALES_SALES_MASTER M,
                       APPAUTH_EMPLOYEES E
                 WHERE     TO_CHAR (INVOICE_DATE, 'MON-YYYY') = P_MONTH_YEAR
                       AND M.EMPLOYEE_ID = E.EMPLOYEE_ID) E
      GROUP BY EMPLOYEE_ID, SALES_MONTH;

   w_sql_stat :=
         'INSERT INTO hrm_salary_sheet ( branch_code ,
dept_id ,
desig_name ,
EMPLOYEE_ID,
employee_name ,
total_atten ,
salary_gross ,
house_rent ,
travel_allowance ,
pf_cutting ,
welfare_cutting,
SALES_COMISSION,
total_advance ,
others_allowance ,
others_deduction ,
stamp_ded_amount ,
total_salary ,
netpay ,
month_year,
app_user_id,app_data_time)
SELECT branch_code,
dept_id,
DESIG_NAME,
EMPLOYEE_ID,
EMPLOYEE_NAME,
TOTAL_ATTEN,
SALARY_GROSS,
house_rent,
travel_allowance,
pf_cutting,
welfare_cutting,
SALES_COMISSION,
TOTAL_ADVANCE,
OTHERS_ALLOWANCE,
OTHERS_DEDUCTION,
STAMP_DED_AMOUNT,
ROUND( COALESCE(SALARY_GROSS,0) + COALESCE (SALES_COMISSION,0)+COALESCE(house_rent,0) + COALESCE (OTHERS_ALLOWANCE,0)+travel_allowance )TOTAL_SALARY,
ROUND( COALESCE(SALARY_GROSS,0) + COALESCE (SALES_COMISSION,0)+COALESCE(house_rent,0) + COALESCE (OTHERS_ALLOWANCE,0)+travel_allowance)
- ROUND((COALESCE(TOTAL_ADVANCE,0) + COALESCE(OTHERS_DEDUCTION,0) + COALESCE(STAMP_DED_AMOUNT,0)+pf_cutting+welfare_cutting))
NETPAY,'''
      || p_month_year
      || ''', '''
      || p_app_user_id
      || ''','''
      || v_time
      || '''
FROM (SELECT branch_code,
department_id dept_id, D.DESIG_NAME,EMPLOYEE_ID,
E.EMPLOYEE_NAME,
TO_CHAR(CAST (
date_trunc (''month'', CAST(''01''||''-''||'''
      || p_month_year
      || ''' AS DATE) )
+ INTERVAL ''1 months''
- INTERVAL ''1 day'' AS DATE),''DD'') TOTAL_ATTEN,
COALESCE( E.basic_salary,0) SALARY_GROSS,
COALESCE( house_rent,0) house_rent,
COALESCE (travel_allowance,0) travel_allowance,
COALESCE(pf_cutting,0) pf_cutting,
COALESCE(welfare_cutting,0) welfare_cutting,

COALESCE (
(SELECT SUM(AMOUNT)
FROM HRM_ADVANCE_SALARY
WHERE EMPLOYEE_ID_ID =EMPLOYEE_ID
AND TO_CHAR(MONTH_YEAR,''MON-YYYY'')= '''
      || p_month_year
      || '''),
0)
TOTAL_ADVANCE,
D.STAMP_DED_AMOUNT,
COALESCE (
(SELECT SUM(AMOUNT)
FROM HRM_ALLOWANCE_PAYMENT
WHERE EMPLOYEE_ID_ID = EMPLOYEE_ID
AND TO_CHAR(MONTH_YEAR,''MON-YYYY'') = '''
      || p_month_year
      || '''),
0)
OTHERS_ALLOWANCE,
COALESCE (
(SELECT SUM(AMOUNT)
FROM HRM_OTHERS_DEDUCTION
WHERE EMPLOYEE_ID_ID = EMPLOYEE_ID
AND TO_CHAR(MONTH_YEAR,''MON-YYYY'') = '''
      || p_month_year
      || '''),
0)
OTHERS_DEDUCTION,COALESCE (
(SELECT total_price*sales_comission/100
FROM sales_sales_commission
WHERE EMPLOYEE_ID = EMPLOYEE_ID
AND sales_month = '''
      || p_month_year
      || '''),
0)
SALES_COMISSION
FROM appauth_employees E, HRM_EMPLOYEE_DESIGNATION D
WHERE E.desig_id = D.DESIG_ID) F where 1=1 ';

   IF p_branch_code IS NOT NULL
   THEN
      w_sql_stat :=
         w_sql_stat || ' AND branch_code= ''' || p_branch_code || '''';
   END IF;

   /*IF p_dept_id IS NOT NULL
   THEN
   w_sql_stat :=
   w_sql_stat || ' AND dept_id= ''' || p_dept_id || '''';
   END IF; */
   --- RAISE EXCEPTION USING MESSAGE = w_sql_stat;
   EXECUTE w_sql_stat;

   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      IF w_status = 'E'
      THEN
         o_status := w_status;
         o_errm := w_errm;
      ELSE
         o_status := 'E';
         o_errm := SQLERRM;
      END IF;
END;
$$;


