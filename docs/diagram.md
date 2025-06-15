graph TD
    subgraph "Windows OS Layer"
        A[Procesos del Sistema]
        B[Sistema de Archivos]
        C[Registro de Windows]
        D[Red]
        E[Usuarios y Permisos]
    end

    subgraph "Core Collection Layer"
        F[Monitor de Procesos]
        G[Monitor de Archivos]
        H[Monitor de Registro]
        I[Monitor de Red]
        J[Monitor de Usuarios]
        K[Event Bus]
    end

    subgraph "Processing Layer"
        L[Feature Extractor]
        M[Event Correlator]
        N[Risk Analyzer]
    end

    subgraph "AI Layer"
        O[Modelo de Clasificación]
        P[Sistema XAI]
        Q[Feedback Loop]
    end

    subgraph "Presentation Layer"
        R[API REST]
        S[Logger]
        T[Dashboard]
        U[Alertas en Tiempo Real]
    end

    %% Conexiones OS Layer -> Core Collection
    A -->|Raw Data| F
    B -->|File Events| G
    C -->|Registry Events| H
    D -->|Network Events| I
    E -->|User Events| J

    %% Event Bus
    F & G & H & I & J -->|Events| K

    %% Processing Flow
    K -->|Raw Events| L
    L -->|Features| M
    M -->|Correlated Events| N

    %% AI Analysis
    N -->|Risk Patterns| O
    O -->|Predictions| P
    P -->|Explanations| Q
    Q -->|Model Updates| O

    %% Output Flow
    P -->|Alerts| R
    P -->|Logs| S
    R -->|Data| T
    R -->|Notifications| U

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style K fill:#ff9,stroke:#333,stroke-width:2px
    style O fill:#9f9,stroke:#333,stroke-width:2px
    style T fill:#99f,stroke:#333,stroke-width:2px