USE [usernine-db];

CREATE USER UserName FOR LOGIN UserLogin;

ALTER ROLE db_datareader ADD MEMBER UserName;
ALTER ROLE db_datawriter ADD MEMBER UserName;

GRANT SELECT, INSERT, UPDATE, DELETE TO [UserName]; -- Ou as permissões necessárias

EXEC sp_addrolemember 'db_datareader', 'UserName';
EXEC sp_addrolemember 'db_datawriter', 'UserName';
EXEC sp_addrolemember 'db_ddladmin', 'UserName';