"""Pinta a barra de título nativa do Windows com as cores do tema ativo."""

from __future__ import annotations

import sys

from app.themes import Theme


def _hex_to_colorref(hex_color: str) -> int:
    """Converte "#rrggbb" para o formato COLORREF do Windows (0x00BBGGRR)."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return (b << 16) | (g << 8) | r


def apply_title_bar(window, theme: Theme) -> None:
    """No Windows, força a barra de título nativa a usar as cores do tema.

    Por padrão essa barra segue o tema/cor de destaque do Windows do
    usuário — sem isso, o app fica com uma barra de título clara ou com uma
    cor de destaque aleatória (a do tema do SO) "destoando" do resto da UI.
    Usa a API do DWM (DwmSetWindowAttribute), a mesma técnica usada por apps
    como o VS Code para ter uma barra de título consistente com o tema do
    app, independente da máquina.

    Precisa ser chamada depois de `window.show()`: antes disso, `winId()`
    devolve um identificador que é trocado quando a janela é criada de fato.

    DWMWA_CAPTION_COLOR/BORDER_COLOR/TEXT_COLOR só têm efeito no Windows 11
    22H2+; em versões mais antigas, o pior caso é manter só o modo escuro ou
    claro (sem as cores exatas da paleta) — degrada bem, não quebra nada.
    """
    if sys.platform != "win32":
        return

    import ctypes

    hwnd = int(window.winId())
    dwmapi = ctypes.windll.dwmapi

    DWMWA_USE_IMMERSIVE_DARK_MODE = 20  # Windows 10 20H1+ e Windows 11
    DWMWA_USE_IMMERSIVE_DARK_MODE_OLD = 19  # builds mais antigas do Windows 10
    dark_value = ctypes.c_int(1 if theme.is_dark else 0)
    for attribute in (DWMWA_USE_IMMERSIVE_DARK_MODE, DWMWA_USE_IMMERSIVE_DARK_MODE_OLD):
        dwmapi.DwmSetWindowAttribute(hwnd, attribute, ctypes.byref(dark_value), ctypes.sizeof(dark_value))

    # DWMWA_SYSTEMBACKDROP_TYPE = DWMSBT_NONE: desliga o Mica/acrílico do
    # Windows 11, que senão tinge a barra de título com o papel de parede.
    DWMWA_SYSTEMBACKDROP_TYPE = 38
    DWMSBT_NONE = 1
    backdrop_value = ctypes.c_int(DWMSBT_NONE)
    dwmapi.DwmSetWindowAttribute(
        hwnd, DWMWA_SYSTEMBACKDROP_TYPE, ctypes.byref(backdrop_value), ctypes.sizeof(backdrop_value)
    )

    # Desligar o Mica acima pode fazer o Windows parar de arredondar os
    # cantos externos da janela automaticamente — força de volta explicitamente.
    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    DWMWCP_ROUND = 2
    corner_value = ctypes.c_int(DWMWCP_ROUND)
    dwmapi.DwmSetWindowAttribute(
        hwnd, DWMWA_WINDOW_CORNER_PREFERENCE, ctypes.byref(corner_value), ctypes.sizeof(corner_value)
    )

    # Cores exatas do tema em vez da cor de destaque do Windows (que varia de
    # máquina pra máquina). A borda usa a MESMA cor do fundo (em vez do valor
    # especial "sem borda", que nem sempre é respeitado igual em todo
    # Windows) — assim ela sempre fica "invisível", mesclada com a janela.
    DWMWA_BORDER_COLOR = 34
    DWMWA_CAPTION_COLOR = 35
    DWMWA_TEXT_COLOR = 36

    for attribute, hex_color in (
        (DWMWA_BORDER_COLOR, theme.bg_start),
        (DWMWA_CAPTION_COLOR, theme.bg_start),
        (DWMWA_TEXT_COLOR, theme.text),
    ):
        color_value = ctypes.c_uint(_hex_to_colorref(hex_color))
        dwmapi.DwmSetWindowAttribute(hwnd, attribute, ctypes.byref(color_value), ctypes.sizeof(color_value))

    # Força o Windows a recalcular/redesenhar a área não-cliente agora, em
    # vez de só na próxima vez que a janela for movida/redimensionada.
    SWP_NOMOVE, SWP_NOSIZE, SWP_NOZORDER, SWP_FRAMECHANGED = 0x0002, 0x0001, 0x0004, 0x0020
    ctypes.windll.user32.SetWindowPos(
        hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED
    )
