
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
 check on the timestamp not in the future is done. This check can be disabled from the configuration file.
  
  Others checks should consider the following cases:
   - Absent fields (machine, ts, load_rate, mileage) or incorrect data type
   - negative mileage, load_rate not between 0 and 100
   - fields with NaN. we should define what is the behavior here (skip the message?)
 
 ## Asynchronous task
 Messages are stored in an intermediate structure before being aggregated and written to the database. 
I used dictionary containing the list of messages to aggregate for each minute. Then I used pandas 
for the easy API for aggregation `groupby` and sql writing `to_sql`. The dictionary structure is cleared each minutes
 from the messages of the previous minute that were aggregated. I do not stored message directly in a pandas data frame
 as appending new rows in pandas is not efficient due to memory reallocation.
 
 
 The aggregation/sql writing is done asynchronously using multithreading, which is limited to a single process in Python due to
 the limitation of the Python interpreter that allows executing one statement at a time (Global Interpreter Lock).
 For scaling purpose, and if the machine running the code has several CPUs, we could using multiple process to digest the messages by having one
 process for each machine messages for example (or by using a round robin hashing to digest multiple machine messages in the same process).
 Another solution could be using third party libraries for handling asynchronous tasks such as Celery or using Async IO.
  
 
 # Testing
 - We should create fake broker for unit test where the results are known. It should include special cases to check 
 message integrity and using different time zones
 
 # Why python?
 I used Python for this exercise mainly because it is easy to prototype with this language and it is the main language used at InUse. 
 I am more comfortable in concurrency and multithreading in Java but the challenge was interesting :)