def extract_from_sql():
    print("Extrayendo datos desde SQL...")

    load_dotenv()

    driver = os.getenv("DB_DRIVER", "").strip()
    server = os.getenv("DB_SERVER", "").strip()
    database = os.getenv("DB_NAME", "").strip()
    user = os.getenv("DB_USER", "").strip()
    password = os.getenv("DB_PASSWORD", "").strip()

    if not driver:
        raise ValueError("Falta DB_DRIVER en .env (ej: ODBC Driver 18 for SQL Server)")
    if not server:
        raise ValueError("Falta DB_SERVER en .env")
    if not database:
        raise ValueError("Falta DB_NAME en .env")
    if not user:
        raise ValueError("Falta DB_USER en .env")
    if not password:
        raise ValueError("Falta DB_PASSWORD en .env")

    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=60;"
    )

    conn = pyodbc.connect(conn_str, autocommit=True)
    conn.timeout = 120
    print("Conectado OK a", database)

    query_path = Path("sql") / "query1.txt"
    query = query_path.read_text(encoding="utf-8")

    df = pd.read_sql(query, conn)
    print(f"Registros extraídos: {len(df)}")
    return df


