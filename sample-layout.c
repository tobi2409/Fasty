#include <windows.h>

// Globale Variablen für die Panel-Handles
HWND hwndLeft, hwndRight, hwndTop, hwndBottom, hwndCenter, hwndChild;

// Fensterprozedur
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;

        case WM_SIZE: {
            int width = LOWORD(lParam);
            int height = HIWORD(lParam);

            // Größe der Panels festlegen
            int panelSize = 100; // feste Größe für linkes, rechtes, oberes, unteres Panel
            int centerSize = 150; // feste Größe für das mittlere Panel

            // Linksausgerichtetes Panel
            MoveWindow(hwndLeft, 0, 0, panelSize, height, TRUE);

            // Rechtsausgerichtetes Panel
            MoveWindow(hwndRight, width - panelSize, 0, panelSize, height, TRUE);

            // Oben ausgerichtetes Panel
            MoveWindow(hwndTop, 0, 0, width, panelSize, TRUE);

            // Unten ausgerichtetes Panel
            MoveWindow(hwndBottom, 0, height - panelSize, width, panelSize, TRUE);

            // Zentriertes Panel
            MoveWindow(hwndCenter, (width - centerSize) / 2, (height - centerSize) / 2, centerSize, centerSize, TRUE);

            // Child-Panel im zentrierten Panel
            MoveWindow(hwndChild, 20, 20, 50, 50, TRUE);
            return 0;
        }
    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    const char CLASS_NAME[] = "Win32PanelsClass";

    // Fensterklasse definieren
    WNDCLASS wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;

    RegisterClass(&wc);

    // Fenster erstellen
    HWND hwnd = CreateWindowEx(
        0,
        CLASS_NAME,
        "Win32 Panels Layout",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
        NULL, NULL, hInstance, NULL
    );

    if (hwnd == NULL) {
        return 0;
    }

    // Panels erstellen und in Variablen speichern
    hwndLeft = CreateWindow("STATIC", "Left Panel", WS_VISIBLE | WS_CHILD | SS_CENTER, 0, 0, 100, 600, hwnd, (HMENU) 1, hInstance, NULL);
    hwndRight = CreateWindow("STATIC", "Right Panel", WS_VISIBLE | WS_CHILD | SS_CENTER, 700, 0, 100, 600, hwnd, (HMENU) 2, hInstance, NULL);
    hwndTop = CreateWindow("STATIC", "Top Panel", WS_VISIBLE | WS_CHILD | SS_CENTER, 0, 0, 800, 100, hwnd, (HMENU) 3, hInstance, NULL);
    hwndBottom = CreateWindow("STATIC", "Bottom Panel", WS_VISIBLE | WS_CHILD | SS_CENTER, 0, 500, 800, 100, hwnd, (HMENU) 4, hInstance, NULL);
    hwndCenter = CreateWindow("STATIC", "Center Panel", WS_VISIBLE | WS_CHILD | SS_CENTER, 325, 225, 150, 150, hwnd, (HMENU) 5, hInstance, NULL);

    // Erstellen eines Child-Panels im Center-Panel
    hwndChild = CreateWindow("STATIC", "Child Panel", WS_VISIBLE | WS_CHILD | SS_CENTER, 20, 20, 50, 50, hwndCenter, NULL, hInstance, NULL);

    ShowWindow(hwnd, nCmdShow);

    // Nachrichtenverarbeitung
    MSG msg = {0};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}
