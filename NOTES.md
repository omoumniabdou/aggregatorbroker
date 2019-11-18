# SQL writing
- maintain an opened connection
- cache prepared statement or eventually use stored procedure
- password should not be declared in infile (we should use a secret manager or encrypt it)

- for the loading_rate table, the order of the composite primary key (machine, ts) should depends on the type
 of queries that we be used on the table as it affects the index lookup efficiency.
 -pandas' DataFrame to_sql is well known to be inefficient. A proper way to write the data to the database is 
 using prepared statement with batch writing
  
 # Handling messages
 ## Message integrity
 Message should be checked before added to the list of messages to aggregate. In the current implementation, only a 
 check on the timestamp not in the future is done. Others checks should consider the following cases:
   - absent fields (machine, ts, load_rate, mileage)
   - negative mileage, load_rate not between 0 and 100
   - fields with NaN. we should define what is the behavior here (skip the message?)

 
 ## Asynchronous task
 - We could use Celery or Air flow to process the messages. for example, we could use batches in Celery to be executed 
 each minute.
 - Async IO could also be used here to deal with asynchronous agregation/SQL writing
 
 
 # Testing
 - We should create fake broker for unit test where the results are known. It should include special cases to check message integrity, 
 using different time zones