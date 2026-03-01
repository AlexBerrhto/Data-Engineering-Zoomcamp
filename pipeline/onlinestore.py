import click
import pandas as pd
from sqlalchemy import create_engine,text
from tqdm.auto import tqdm


@click.command()
@click.option('--file_name', default='online_retail_II.xlsx', help='Path to Excel file')
@click.option('--pg_user', default='root', help='Postgres username')
@click.option('--pg_pass', default='root', help='Postgres password')
@click.option('--pg_host', default='localhost', help='Postgres host')
@click.option('--pg_port', default=5432, help='Postgres port')
@click.option('--pg_db', default='online_store', help='Database name')
@click.option('--target_table', default='retail_data', help='Target table name')
@click.option('--chunksize', default=10000, help='Upload chunk size')
def run(file_name,pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, chunksize):
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Manually create the table with the correct types
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS retail_data"))
        conn.execute(text("""
            CREATE TABLE retail_data (
                invoice TEXT,
                stockcode TEXT,
                description TEXT,
                quantity BIGINT,
                invoicedate TIMESTAMP WITHOUT TIME ZONE,
                price FLOAT(53),
                customer_id BIGINT,
                country TEXT
            )
        """))
        conn.commit()


   
    xl = pd.ExcelFile(file_name)
    sheet_names = xl.sheet_names

    all_dfs = [xl.parse(s) for s in xl.sheet_names]

    print("Combining sheets...")
    df_all = pd.concat(all_dfs, ignore_index=True)

    df_all.columns = [c.lower().replace(" ", "_") for c in df_all.columns]

    chunk_size = chunksize
    print(f"Starting batch upload of {len(df_all)} rows...")

    for i in tqdm(range(0, len(df_all), chunk_size)):
        # Take a slice of the data
        df_chunk = df_all.iloc[i : i + chunk_size]

        # Use 'append' so we don't delete the table you just manually created!
        df_chunk.to_sql(
            name= target_table, 
            con=engine, 
            if_exists='append', 
            index=False
        )

    print("Batch processing complete!")

if __name__ == '__main__':
    run()


