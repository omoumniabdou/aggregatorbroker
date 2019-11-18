# SQL writing
- maintain an opened connection
- cache prepared statement or eventually use stored procedure
- password should not be declared in infile (we should use a secret manager or encrypt it)

- for the loading_rate table, the order of the composite primary key (machine, ts) should depends on the type
 of queries that we be used on the table as it affects the index lookup efficiency.
  
 # Handling messages
 ## remove false data
 - I compared the timestamp of the payload with the 'now' datetime. 
 
 ## Asynchronous task
 - We could use Celery or Air flow to process the messages. for example, we could use batches in Celery to be executed 
 each minute.
 - Async IO could also be used here to deal with asynchronous agregation/SQL writing
 
 
 # Testing
 - We should create fake broker for unit test