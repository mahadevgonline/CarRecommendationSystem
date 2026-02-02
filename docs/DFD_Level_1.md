# DFD Level-1: Online Car Recommendation System (Simplified)

This diagram represents the Level-1 Data Flow for the system, designed for simplicity and readability. It follows a linear flow from **Entities** to **Processes** to **Data Stores**.

```mermaid
graph LR
    %% -- ENTITIES (Left) --
    User[User]
    Seller_Ent[Seller]
    Admin[Admin]

    %% -- PROCESSES (Middle) --
    Auth((Authentication))
    CarMgmt((Car Mgmt))
    Shop((Shopping))
    PartMgmt((Part Mgmt))
    OrderOps((Order Ops))
    SellerAdmin((Seller Admin))

    %% -- DATA STORES (Right) --
    DB_Users[(Users/Sellers)]
    DB_Cars[(Cars)]
    DB_Parts[(Parts)]
    DB_Cart[(Cart)]
    DB_Orders[(Orders)]
    DB_Notifs[(Notifications)]

    %% -- FLOWS --

    %% 1. Auth Flow
    User & Seller_Ent & Admin -->|Credentials| Auth
    Auth <-->|Verify & Profile| DB_Users

    %% 2. Car Management
    Admin -->|Add/Edit Cars| CarMgmt
    CarMgmt <-->|Car Data| DB_Cars
    Auth -.->|Access| CarMgmt

    %% 3. Shopping Flow
    User -->|Browse & Search| Shop
    Shop <-->|Fetch Details| DB_Cars
    Shop <-->|Fetch Details| DB_Parts
    User -->|Add to Cart| Shop
    Shop <-->|Store Items| DB_Cart

    %% 4. Part Management
    Seller_Ent -->|Manage Parts| PartMgmt
    PartMgmt <-->|Part Data| DB_Parts
    
    %% 5. Order Operations
    User -->|Checkout| OrderOps
    Seller_Ent -->|Update Status| OrderOps
    OrderOps -->|Save Order| DB_Orders
    OrderOps -->|Notify User| DB_Notifs
    DB_Notifs -->|Read| User

    %% 6. Seller Admin
    Admin -->|Approve Sellers| SellerAdmin
    SellerAdmin -->|Update Status| DB_Users

    %% Styling for "Reference" Look
    classDef process fill:#fff,stroke:#000,stroke-width:2px;
    classDef store fill:#f9f9f9,stroke:#000,stroke-width:2px,shape:cylinder;
    classDef entity fill:#fff,stroke:#000,stroke-width:2px;

    class Auth,CarMgmt,Shop,PartMgmt,OrderOps,SellerAdmin process;
    class DB_Users,DB_Cars,DB_Parts,DB_Cart,DB_Orders,DB_Notifs store;
    class User,Seller_Ent,Admin entity;
```
