# SQL writing
I used pandas `to_sql` method for simplicity. However it is well known to be inefficient. One should prefer using the following:
- maintain an opened connection (use a pool if we aggregate a lot of data asynchronously)
- cache prepared statement or eventually use stored procedure
- Depending on the number of machines, we could also use batches (bulk insert) with potentially a max batch size 
depending on the bandwidth and the latency between the client and the database server.
- password should not be declared in configuration file (we should use a secret manager or encrypt it)
- for the loading_rate table, the choice of the primary key and eventually the indexes to add (also the order of the
 primary key if it is a composite primary key) should depends on the type of queries that will be used. I chose
a composite primary key (machine, ts) but this can be discussed.
  
 # Handling messages
 ## Message integrity
 Message should be checked before added to the list of messages to aggregate. In the current implementation, only a 
 check on the timestamp not in the future is done. Others checks should consider the following cases:
   - Absent fields (machine, ts, load_rate, mileage) or incorrect data type
   - negative mileage, load_rate not between 0 and 100
   - fields with NaN. we should define what is the behavior here (skip the message?)
 
 ## Asynchronous task
 - We could use Celery or Air flow to process the messages. For example, we could use batches in Celery to be executed 
 each minute.
 - Async IO could also be used here to deal with asynchronous aggregation/SQL writing
 
 
 # Testing
 - We should create fake broker for unit test where the results are known. It should include special cases to check 
 message integrity and using different time zones