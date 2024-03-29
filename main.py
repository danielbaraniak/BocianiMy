import PySimpleGUI as sg
import geoanalysis as g
from fiona import _shim, schema # for PyInstaller

# sg.theme("DarkAmber")
sg.theme("SystemDefault1")


df = []
tc = []
stops = None

loading_spinner = "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"


def stops_wrapper(filtered_df, min_duration_h, max_diameter, include_corine):
    global stops
    stops = g.detect_stops(
        g.get_trajectory_collection(filtered_df),
        min_duration_h=int(min_duration_h),
        max_diameter=int(max_diameter),
        include_corine=include_corine,
    )


layout = [
    [sg.Text("Folder z plikami csv")],
    [
        sg.Input(key="-IN_FILES-"),
        sg.FilesBrowse(
            file_types=(("CSV", "*.csv"),),
        ),
    ],
    [sg.Button("Otwórz")],
    [
        sg.Table(
            values=[[]],
            headings=[
                "device_id",
                "Latitude",
                "Longitude",
                "timestamp",
            ],
            vertical_scroll_only=False,
            visible=False,
            key="-PREVIEW_TABLE-",
        ),
        sg.Listbox(
            values=[],
            size=(30, 6),
            select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
            visible=False,
            key="deviceIdListbox",
        ),
    ],
    [
        sg.Text("Średnica obszaru:", size=20),
        sg.Input(
            key="-MAX_DIAMETER-",
            default_text=10000,
            size=6,
            justification="right",
            enable_events=True,
        ),
        sg.Text("m"),
    ],
    [
        sg.Text("Minimalny czas postoju:", size=20),
        sg.Input(
            key="-MIN_DURATION-",
            default_text=48,
            size=6,
            justification="right",
            enable_events=True,
        ),
        sg.Text("h"),
    ],
    [
        sg.Button("Znajdź przystanki", key="stopDetect", disabled=True),
        sg.Checkbox("Dołącz dane z CORINE", key="-INCLUDE_CORINE-"),
    ],
    [
        sg.Table(
            values=df,
            headings=[
                "geometry",
                "start_time",
                "end_time",
                "traj_id",
                "duration_h",
                "corine_label_id",
                "corine_label_text",
            ],
            vertical_scroll_only=False,
            visible=False,
            display_row_numbers=True,
            key="-STOPS_TABLE-",
        ),
    ],
    [
        sg.Input(key="-OUT_DIRNAME-"),
        sg.FileSaveAs(
            default_extension="gpx",
            file_types=(
                ("GeoPackage", "*.gpkg"),
                # ("GPX", "*.gpx"),
                ("GeoJson", "*.geojson"),
            ),
        ),
    ],
    [sg.Button("Zapisz", disabled=True)],
]


def main():
    # Create the Window
    window = sg.Window("Miejsca postojów", layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break

        if event == "Otwórz" and values["-IN_FILES-"] != "":
            df = g.import_data(file_list=values["-IN_FILES-"].split(";"))
            if df is not None:
                window["-PREVIEW_TABLE-"].update(
                    visible=True,
                    values=df.values.tolist(),
                )
                window["deviceIdListbox"].update(
                    visible=True, values=g.get_device_ids(df)
                )
                window["stopDetect"].update(disabled=False)
            else:
                sg.popup("Nie można odczytać pliku")

        if event == "stopDetect":
            window["-PREVIEW_TABLE-"].update(
                values=df[
                    df["device_id"].isin(values["deviceIdListbox"])
                ].values.tolist(),
            )
            sg.popup_animated(image_source=loading_spinner, message="loading...")
            window.refresh()
            filtered_df = df[df["device_id"].isin(list(values["deviceIdListbox"]))]
            window.perform_long_operation(
                lambda: stops_wrapper(
                    filtered_df,
                    min_duration_h=int(values["-MIN_DURATION-"]),
                    max_diameter=int(values["-MAX_DIAMETER-"]),
                    include_corine=values["-INCLUDE_CORINE-"],
                ),
                "-END KEY-",
            )
        if event == "-END KEY-":
            window["-STOPS_TABLE-"].update(visible=True, values=stops.values.tolist())
            window["Zapisz"].update(disabled=False)

            sg.popup_animated(image_source=None)
            window.refresh()

        if event == "Zapisz" and values["-OUT_DIRNAME-"] != "" and stops is not None:
            g.save_to_file(df=stops, filename=values["-OUT_DIRNAME-"])
            sg.popup(f"Zapisano do: {values['-OUT_DIRNAME-']}")

    window.close()


if __name__ == "__main__":
    main()
