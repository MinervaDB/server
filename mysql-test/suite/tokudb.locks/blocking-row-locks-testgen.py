# 9/23/2011 Generate blocking row lock tests
import datetime

# generate sql write queries
def mysqlgen_select_for_update(k, kv):
    print "select * from t where %s=%s for update;" % (k, kv)
def mysqlgen_update(k, kv, c, cv):
    print "update t where %s=%s set %s=%s+1;" % (k, kv, kv, kv);
def mysqlgen_insert(k, kv, c, cv):
    print "insert t values(%s, %s);" % (kv, cv)
def mysqlgen_replace(k, kv, c, cv):
    print "replace t values(%s, %s);" % (kv, cv)

# genrate sql read queries
def mysqlgen_select_star():
    print "select * from t;"
def mysqlgen_select_where(where):
    print "select * from t where %s;" % where

# mysql test code generation
def mysqlgen_prepare():
    print "# prepare with some common parameters"
    print "set storage_engine=tokudb;"
    print "connect(conn1, localhost, root);"
    # ONLY connection 1 should have autocommit off.
    print "set autocommit=off;"
    print "connect(conn2, localhost, root);"
    print "connection conn1;"
    print ""
def mysqlgen_reload_table():
    print "# drop old table, generate new one. 4 rows"
    print "--disable_warnings"
    print "drop table if exists t;"
    print "--enable_warnings"
    print "create table t (a int primary key, b int);"
    for i in range(1, 5):
        mysqlgen_insert("a", i, "b", i*i)
    print ""
def mysqlgen_cleanup():
    print "# clean it all up"
    print "drop table t;"
    print "set global tokudb_lock_timeout=30000000;"
    print ""

# Here's where all the magic happens
print "# Tokutek"
print "# Blocking row lock tests;"
print "# Generated by %s on %s;" % (__file__, datetime.date.today())
print ""
print "# BEGIN WRITE/WRITE CONFLICTS TESTS"
print ""

# Iterate through all possible situations. Each timeout class,
# each pair of write queries, each kind of query.
write_queries = [
        ("select for update", mysqlgen_select_for_update),
        ("update", mysqlgen_update),
        ("insert", mysqlgen_insert),
        ("replace", mysqlgen_replace) ]
mysqlgen_prepare()
mysqlgen_reload_table()
for timeout in ["0", "1000000"]:
    print "# testing with timeout %s" % timeout
    print "set global tokudb_lock_timeout=%s;" % timeout
    print ""
    for ta, qa in write_queries:
        for tb, qb in write_queries:
            print "# testing conflict \"%s\" vs. \"%s\"" % (ta, tb)
            print "connection conn1;"
            print "begin;"
            print ""

            # point lock
            print "#TODO: Test point lock"
            print ""

            # range lock
            print "#TODO: Test range lock"
            print ""

            # overlapping range
            print "#TODO: Test overlapping range locks"
            print ""
            
            # Always check in the end that a commit
            # allows the other transaction full access
            print "connection conn1;"
            print "commit;"
            print "connection conn2;"
            mysqlgen_select_star()
            print "connection conn1;"
            print ""
mysqlgen_cleanup()
