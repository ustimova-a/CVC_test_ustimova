## SQL TEST USTIMOVA (CVC)

### Задание 1

Напишите запрос, который вывел бы номер документа, дату создания и создателя записи для всех строк из таблицы StkDocs .

#### Решение

    SELECT NumDoc, DateWrt, Creator
    FROM StkDocs;

### Задание 2
Напишите запросы, которые вывели бы:

*Наименования всех контрагентов, у которых имеется телефон (таблицы Contras и Telct ) и поле Respondent пустое.*
 
    SELECT Contras.Nm_Ct FROM Contras 
    LEFT JOIN Telct ON Contras.CodCt = Telct.CodCt 
    WHERE Telct.TelNum <> '' AND Telct.Respondent = '' 
    GROUP BY Nm_Ct;
    

> В результате этого запроса выводится один контрагент, у которого есть два разных номера телефона, но поле Respondent пустое только у одного.

*Наименования всех контрагентов и телефоны для тех из них, у которых он существует.*

    SELECT Contras.Nm_Ct, Telct.TelNum
    FROM Contras 
    LEFT JOIN Telct ON Contras.CodCt = Telct.CodCt;

*Наименование и количество указанных телефонов тех контрагентов, у которых указано более одного телефона.*

    SELECT Contras.Nm_Ct, COUNT(Telct.TelNum)
    FROM Contras
    LEFT JOIN Telct ON Contras.CodCt=Telct.CodCt
    GROUP BY Nm_Ct
    HAVING COUNT(Telct.TelNum)>1;

*Наименования контрагентов, у которых не привязано ни одного телефона.*

    SELECT Contras.Nm_Ct
    FROM Contras
    LEFT JOIN Telct ON Contras.CodCt = Telct.CodCt
    WHERE Telct.TelNum is NULL;

### Задание 3

Напишите запрос, который может дать вам все записи со значениями суммы в поле SummaGdSrv больше чем 1,500.( таблица StkDocsGdsAndSrv ).

#### Решение

    SELECT SummaGdSrv 
    FROM StkDocsGdsAndSrv
    WHERE SummaGdSrv>1500;


### Задание 4

Напишите запрос, который выведет номера всех документов, суммы которых больше 3000, но меньше 6000 (Таблицы StkDocsGdsAndSrv и StkDocs).

#### Решение

    SELECT StkDocs.CodDoc
    FROM StkDocs
    LEFT JOIN StkDocsGdsAndSrv on StkDocsGdsAndSrv.CodDoc=StkDocs.CodDoc
    GROUP BY StkDocs.CodDoc
    HAVING SUM(StkDocsGdsAndSrv.SummaGdSrv) > 3000
    AND SUM(StkDocsGdsAndSrv.SummaGdSrv) < 6000;

### Задание 5

Что может быть выведено в результате следующего запроса?

    SELECT *
    FROM StkDocs
    WHERE (NumDoc < ‘10000’ OR NOT (DateWrt=to_date(’10.03.2001’,’dd.mm.yyyy’)
    AND Creator = “SYSADM”))

#### Решение
В результате данного запроса будет выведена вся таблица.

### Задание 6

Напишите запрос, который может вывести всех контрагентов чьи имена начинаются с буквы попадающей в диапазон от A до К (таблица Contras ).

#### Решение

    SELECT Nm_Ct
    FROM Contras
    WHERE Nm_Ct ~ '^[А-К]';

### Задание 7

Напишите запрос, который сосчитал бы всю сумму поля SummaGdSrv на 01 июня 2005 года (поле DateWr таблицы StkDocs) из таблиц StkDocs и StkDocsGdsAndSrv тех документов, которые созданы пользователями LOBUC и DES.

#### Решение

    SELECT SUM(StkDocsGdsAndSrv.SummaGdSrv)
    FROM StkDocsGdsAndSrv
    LEFT JOIN StkDocs on StkDocsGdsAndSrv.CodDoc = StkDocs.CodDoc
    WHERE StkDocs.DateWrt <= '2005-06-01'::date AND
    (StkDocs.Creator = 'LOBUC' or StkDocs.Creator = 'DES');


### Задание 8

Напишите запрос, который вывел бы по каждому товару его остаток на складе (Таблица StkDocsGdsAndSrv) на дату 01 июня 2005 г. (поле DateWrt таблицы StkDocs).

#### Решение

    SELECT StkDocsGdsAndSrv.CodGdSrv, StkDocsGdsAndSrv.QtyGdSrv
    FROM StkDocsGdsAndSrv
    LEFT JOIN StkDocs ON StkDocsGdsAndSrv.CodDoc = StkDocs.CodDoc
    WHERE StkDocs.DateWrt <= '2005-06-01'::date;

### Задание 9

К любому документу могут быть привязаны определенные аналитические признаки – элементы пользовательских справочников (таблицы StkDocsRef и RefItem). Напишите следующие запросы:

*Запрос, который выведет для всех документов, привязанные к ним аналитические признаки в виде следующей таблицы:*
| Номер документа | Дата документа | Наименование справочника | Наименование значения |
|--|--|--|--|

    SELECT StkDocs.NumDoc, StkDocs.DateWrt, RefItem.NmInRef, Refs.NmRef
    FROM StkDocsRef
    LEFT JOIN StkDocs ON StkDocsRef.CodDoc = StkDocs.CodDoc
    LEFT JOIN RefItem ON StkDocsRef.CodInRef = RefItem.CodInRef
    LEFT JOIN Refs ON StkDocsRef.CodRef = Refs.CodRef;

*Запрос, который выведет все документы, имеющие аналитический признак «Розничные продажи» по справочнику «Вид реализации».*

    SELECT StkDocs.*
    FROM StkDocsRef
    LEFT JOIN StkDocs ON StkDocsRef.CodDoc = StkDocs.CodDoc
    LEFT JOIN RefItem ON StkDocsRef.CodInRef = RefItem.CodInRef
    LEFT JOIN Refs ON StkDocsRef.CodRef = Refs.CodRef
    WHERE Refs.NmRef = 'Вид реализации' AND
    RefItem.NmInRef = 'Розничные продажи';

*Запрос, который вывел бы количество документов, имеющих аналитический признак по справочнику «Статус документа» и количество документов, не имеющих такого признака.*

    SELECT COUNT(StkDocsRef.CodDoc)
    FROM StkDocsRef
    LEFT JOIN Refs ON StkDocsRef.CodRef = Refs.CodRef
    WHERE Refs.NmRef = 'Статус документа'
    UNION
    SELECT COUNT(StkDocsRef.CodDoc)
    FROM StkDocsRef
    LEFT JOIN Refs ON StkDocsRef.CodRef=Refs.CodRef
    WHERE Refs.NmRef <> 'Статус документа';

*Запрос, выводящий список ВСЕХ (как имеющих аналитический признак, так и не имеющих) документов с наименованием привязанной аналитики для тех документов, у которых есть аналитический признак по справочнику «Вид реализации». Выводить привязанные значения по другим аналитическим справочникам ненужно.*

    SELECT StkDocs.*, (CASE WHEN Refs.NmRef <> 'Вид реализации'
    THEN  ''  
    ELSE  Refs.NmRef  
    END)  
    FROM  StkDocsRef  
    LEFT JOIN StkDocs ON StkDocsRef.CodDoc = StkDocs.CodDoc  
    LEFT JOIN Refs ON StkDocsRef.CodRef = Refs.CodRef

### Задание 10

Создайте триггер, который при изменении значение поля SummaGdSrv из таблицы StkDocsGdsAndSrv заполнял поля таблицы AlfaAudit в соответствие с описанием полей таблицы AlfaAudit.

#### Решение

    CREATE OR REPLACE FUNCTION public.updatePrices()
    RETURNS trigger
    LANGUAGE plpgsql
    AS $function$
	    BEGIN
		    INSERT INTO AlfaAudit (TriggerName, CodGdSrv, DbUser, DateChange, OldPrice, NewPrice)
		    SELECT 'PrcGdSrv_Update', CodGdSrv, USER, CURRENT_DATE, OLD.PrcGdSrv, NEW.PrcGdSrv
		    FROM StkDocsGdsAndSrv
		    WHERE id = OLD.id;
		    RETURN NULL;
	    END;
        $function$
    
    CREATE OR REPLACE TRIGGER PrcGdSrv_Update
    AFTER UPDATE OF PrcGdSrv ON StkDocsGdsAndSrv
    FOR EACH ROW EXECUTE PROCEDURE updatePrices();

> В задании говорилось об изменении поля SummaGdSrv (сумма). Однако также в задании указано, что в таблицу AlfaAudit требуется вносить старые и новые значения поля PrcGdSrv (цена). На первый взгляд, звучит двойственно - либо тут опечатка в названии первого поля (SummaGdSrv), либо действительно указано при изменении поля суммы пересчитывать новую цену с учётом количества указанного товара и уже её вносить в таблицу AlfaAudit. Второе показалось надуманным и оверинжинирингом, поэтому пока сделала по первому варианту.

### Задание 11
Сформировать запрос, который вывел бы последовательность из начальных дат 12 месяцев, начиная от текущего. Например, если текущая дата 13.09.2017, то запрос должен вывести:

> К сожалению, самостоятельно решить эту задачу я не смогла, но ее
> решение можно найти в гугле:
> https://webhamster.ru/mytetrashare/index/mtb402/1507295009qcmn4lzn05
