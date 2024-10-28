use clap::{Parser, Subcommand}; // Removed CommandFactory as it's not needed for this case
use rusqlite::{Connection, Result};
use sqlite::{create_table, do_all, drop_table, load_data_from_csv, query_exec}; // Import do_all

// Define a struct (or object) to hold our CLI arguments
#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

// An enum to represent subcommands
#[derive(Debug, Subcommand)]
enum Commands {
    /// Pass a table name to create a table
    #[command(alias = "c")]
    Create { table_name: String },

    /// Pass a query string to execute Read or Update operations
    #[command(alias = "q")]
    Query { query: String },

    /// Pass a table name to drop
    #[command(alias = "d")]
    Delete { delete_query: String },

    /// Pass a table name and a file path to load data from CSV
    #[command(alias = "l")]
    Load {
        table_name: String,
        file_path: String,
    },

    /// Pass a table name, a set clause, and a condition to update a row in the table
    #[command(alias = "u")]
    Update {
        table_name: String,
        set_clause: String,
        condition: String,
    },

    /// Perform all steps sequentially with a URL, table name, and file path
    #[command(alias = "a")] // Changed from 'b' to 'a' for clarity
    DoAll {
        url: String,
        table_name: String,
        file_path: String,
    },
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Generate connection
    let conn = Connection::open("my_database.db")?;

    // Here we parse the CLI arguments and store them in the args object
    let args = Cli::parse();

    // Here we can match the behavior on the subcommand and call our lib logic
    match args.command {
        Commands::Create { table_name } => {
            println!("Creating Table {}", table_name);
            create_table(&conn, &table_name).expect("Failed to create table");
        }
        Commands::Query { query } => {
            println!("Query: {}", query);
            query_exec(&conn, &query).expect("Failed to execute query");
        }
        Commands::Delete { delete_query } => {
            println!("Deleting: {}", delete_query);
            drop_table(&conn, &delete_query).expect("Failed to drop table");
        }
        Commands::Load {
            table_name,
            file_path,
        } => {
            println!(
                "Loading data into table '{}' from '{}'",
                table_name, file_path
            );
            load_data_from_csv(&conn, &table_name, &file_path)
                .expect("Failed to load data from csv");
        }
        Commands::Update {
            table_name,
            set_clause,
            condition,
        } => {
            let query = format!(
                "UPDATE {} SET {} WHERE {};",
                table_name, set_clause, condition
            );
            println!("Executing update: {}", query);
            query_exec(&conn, &query).expect("Failed to execute update");
        }
        Commands::DoAll {
            url,
            table_name,
            file_path,
        } => {
            println!("URL: {}, Table: {}, File: {}", url, table_name, file_path);
            do_all(&conn, &url, &table_name, &file_path).expect("Failed to perform all steps");
        }
    }
    Ok(())
}
