#!/usr/bin/env node
/**
 * Execute a SQL query against PostgreSQL via PgBouncer from within a pod.
 *
 * Usage (from kubectl exec):
 *   node query.js --host <pgbouncer-host> --db <database> --sql "SELECT count(*) FROM client"
 *   node query.js --host <pgbouncer-host> --db <database> --sql "SELECT id FROM client WHERE id IN ('uuid1','uuid2')"
 *   node query.js --host <pgbouncer-host> --db <database> --tables
 *   node query.js --host <pgbouncer-host> --db <database> --describe <table>
 *   node query.js --host <pgbouncer-host> --db <database> --exists <table> --ids "uuid1,uuid2,uuid3"
 *
 * Environment:
 *   POSTGRES_PASSWORD - Required, read from pod env
 *   DB_USER - Optional, defaults to "postgres"
 *   DB_PORT - Optional, defaults to 6432
 */

const { Client } = require("pg");

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--host") opts.host = args[++i];
    else if (args[i] === "--db") opts.db = args[++i];
    else if (args[i] === "--port") opts.port = parseInt(args[++i]);
    else if (args[i] === "--user") opts.user = args[++i];
    else if (args[i] === "--sql") opts.sql = args[++i];
    else if (args[i] === "--tables") opts.tables = true;
    else if (args[i] === "--describe") opts.describe = args[++i];
    else if (args[i] === "--exists") opts.exists = args[++i];
    else if (args[i] === "--ids") opts.ids = args[++i];
  }
  return opts;
}

async function main() {
  const opts = parseArgs();

  if (!opts.host || !opts.db) {
    console.error("Usage: node query.js --host <host> --db <database> [--sql <query> | --tables | --describe <table> | --exists <table> --ids <csv>]");
    process.exit(1);
  }

  const client = new Client({
    host: opts.host,
    port: opts.port || parseInt(process.env.DB_PORT) || 6432,
    database: opts.db,
    user: opts.user || process.env.DB_USER || "postgres",
    password: process.env.POSTGRES_PASSWORD,
  });

  try {
    await client.connect();

    let sql;

    if (opts.tables) {
      sql = "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename";
      const r = await client.query(sql);
      console.log(`Tables (${r.rows.length}):`);
      r.rows.forEach((row) => console.log(`  ${row.tablename}`));
    } else if (opts.describe) {
      sql = `SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name = '${opts.describe}' ORDER BY ordinal_position`;
      const r = await client.query(sql);
      console.log(`Columns in ${opts.describe} (${r.rows.length}):`);
      r.rows.forEach((row) =>
        console.log(`  ${row.column_name} | ${row.data_type} | nullable=${row.is_nullable}${row.column_default ? " | default=" + row.column_default : ""}`)
      );
    } else if (opts.exists && opts.ids) {
      const ids = opts.ids.split(",").map((id) => id.trim());
      const inClause = ids.map((id) => `'${id}'`).join(",");
      sql = `SELECT id FROM ${opts.exists} WHERE id IN (${inClause})`;
      const r = await client.query(sql);
      const found = new Set(r.rows.map((x) => x.id));
      const missing = ids.filter((id) => !found.has(id));
      console.log(`Found: ${found.size}/${ids.length}`);
      if (missing.length > 0) {
        console.log(`Missing (${missing.length}):`);
        missing.forEach((id) => console.log(`  ${id}`));
      }
    } else if (opts.sql) {
      const r = await client.query(opts.sql);
      if (r.rows.length === 0) {
        console.log("No rows returned.");
      } else {
        // Print as table
        const cols = Object.keys(r.rows[0]);
        console.log(cols.join(" | "));
        console.log(cols.map((c) => "-".repeat(c.length)).join("-+-"));
        r.rows.forEach((row) => console.log(cols.map((c) => String(row[c] ?? "NULL")).join(" | ")));
        console.log(`\n${r.rows.length} row(s)`);
      }
    } else {
      console.error("Specify --sql, --tables, --describe <table>, or --exists <table> --ids <csv>");
      process.exit(1);
    }
  } catch (e) {
    console.error("Error:", e.message);
    process.exit(1);
  } finally {
    await client.end();
  }
}

main();
