import click
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
import json

TEMPLATE_DIR = (Path(__file__).parent / "templates").resolve()

# --- Databricks Connection Helper ---

def get_spark_session():
    """
    Loads .env file and creates a Databricks Spark session.
    Returns the spark session or None if connection fails.
    """
    load_dotenv()
    
    required_vars = ['DATABRICKS_HOST', 'DATABRICKS_TOKEN', 'WAREHOUSE_ID', 'CATALOG', 'SCHEMA']
    if not all(os.getenv(var) for var in required_vars):
        click.echo("Error: Missing one or more required environment variables in .env file.")
        click.echo(f"Required: {', '.join(required_vars)}")
        return None

    try:
        from databricks.connect import DatabricksSession
        spark = DatabricksSession.builder.sdkConfig(
            host = os.getenv('DATABRICKS_HOST'),
            token = os.getenv('DATABRICKS_TOKEN'),
            cluster_id = os.getenv('WAREHOUSE_ID'),
            catalog = os.getenv('CATALOG'),
            schema = os.getenv('SCHEMA')
        ).getOrCreate()
        return spark
    except Exception as e:
        click.echo(f"Error connecting to Databricks: {e}")
        return None

# --- CLI Command Group ---

@click.group()
def cli():
    """A CLI tool for bootstrapping OODA Loop data science projects."""
    pass

def copy_template_files(template_dir, dest_dir):
    """
    Recursively copies files from the template directory to the destination,
    preserving the directory structure.
    """
    for item in template_dir.iterdir():
        dest_path = dest_dir / item.relative_to(template_dir)
        if item.is_dir():
            dest_path.mkdir(parents=True, exist_ok=True)
            copy_template_files(item, dest_path)
        else:  # It's a file
            item_name = item.name
            dest_file_name = item_name

            if item_name.endswith('.ipynb.txt'):
                dest_file_name = item_name[:-4]
            elif item_name == 'databricks.env':
                dest_file_name = '.env'

            final_dest_path = dest_dir / dest_file_name

            if item_name.endswith('.ipynb.txt'):
                # Special handling for notebooks as they are text templates
                with open(item, 'r') as f:
                    notebook_content = f.read()
                with open(final_dest_path, 'w') as f:
                    f.write(notebook_content)
            else:
                # Normal copy for all other files
                shutil.copy2(item, final_dest_path)

            click.echo(f"  Created file: {final_dest_path.name}")

@cli.command()
def init():
    """Initializes a new data science project."""
    click.echo("Initializing oodaloop DS project...")
    
    project_dir = Path.cwd()
    
    # Create the main directories that might not be in templates
    # (like sql and metadata if we only have .gitkeep placeholders)
    # The recursive copy will handle the rest.
    (project_dir / "sql").mkdir(exist_ok=True)
    (project_dir / "metadata").mkdir(exist_ok=True)
    
    copy_template_files(TEMPLATE_DIR, project_dir)

    click.echo("\nProject initialized successfully!")
    click.echo("Next steps:")
    click.echo("1. Fill out `docs/questionnaire.md`.")
    click.echo("2. Add database schema information to the `metadata` directory.")
    click.echo("3. Start your analysis in `notebooks/exploration.ipynb`.")

# --- New Commands ---

@cli.command()
def auth():
    """Tests the connection to Databricks using credentials from .env file."""
    click.echo("Attempting to authenticate with Databricks...")
    spark = get_spark_session()
    if spark:
        click.echo(click.style("Authentication successful!", fg='green'))
        try:
            user = spark.sql("SELECT current_user()").collect()[0][0]
            click.echo(f"Current user: {user}")
            catalog = os.getenv('CATALOG')
            schema = os.getenv('SCHEMA')
            click.echo(f"Current catalog: {catalog}")
            click.echo(f"Current schema: {schema}")
        except Exception as e:
            click.echo(f"Could not retrieve user info: {e}")
    else:
        click.echo(click.style("Authentication failed. Check .env file and network connection.", fg='red'))

@cli.command()
@click.option('--format', type=click.Choice(['table', 'json']), default='table', help='Output format.')
def list_catalog(format):
    """Lists all available catalogs in the Databricks workspace."""
    spark = get_spark_session()
    if not spark:
        return
    
    try:
        catalogs = spark.catalog.listCatalogs()
        
        if format == 'json':
            click.echo(json.dumps([c.asDict() for c in catalogs], indent=2))
        else: # table format
            click.echo("Available Catalogs:")
            for catalog in catalogs:
                click.echo(f"- {catalog.catalog}")

    except Exception as e:
        click.echo(f"Error listing catalogs: {e}")

@cli.command()
@click.argument('table_name')
def expand_table(table_name):
    """Fetches the schema for a table and saves it to a JSON file."""
    spark = get_spark_session()
    if not spark:
        return

    try:
        click.echo(f"Fetching schema for table: {table_name}")
        schema = spark.table(table_name).schema.jsonValue()
        
        # Ensure metadata directory exists
        metadata_dir = Path('metadata')
        metadata_dir.mkdir(exist_ok=True)
        
        # Sanitize table name for filename
        filename = table_name.replace('.', '_') + '.json'
        filepath = metadata_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(schema, f, indent=2)
            
        click.echo(click.style(f"Successfully wrote schema to {filepath}", fg='green'))

    except Exception as e:
        click.echo(click.style(f"Error expanding table '{table_name}': {e}", fg='red'))

if __name__ == '__main__':
    cli() 