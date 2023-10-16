USE master;

CREATE LOGIN UserLogin WITH PASSWORD = 'password*';

CREATE USER UserName FOR LOGIN UserLogin;