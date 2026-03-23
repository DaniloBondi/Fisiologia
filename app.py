from shiny import App, render, ui, reactive
import numpy as np
import plotly.graph_objects as go

# Configuration dictionaries
TISSUE_DESCRIPTIONS = {
    "cardiac": (
        "Cardiac action potentials have a characteristic long plateau phase (Phase 2) "
        "that lasts 200-300ms. This extended depolarization is due to slow Ca²⁺ channels "
        "and prevents tetanic contractions, ensuring proper heart pumping function. "
        "The five phases are: 0 (rapid depolarization), 1 (early repolarization), "
        "2 (plateau), 3 (repolarization), and 4 (resting potential)."
    ),
    "neuron": (
        "Neuronal action potentials are rapid, lasting only 1-2ms. They feature a sharp "
        "depolarization phase followed by quick repolarization and a brief hyperpolarization "
        "period. This rapid signaling allows neurons to transmit information quickly along "
        "axons. The brief refractory period enables high-frequency firing."
    ),
    "skeletal": (
        "Skeletal muscle action potentials have an intermediate duration of 2-5ms. "
        "They are similar to neuronal action potentials but slightly longer. The action "
        "potential propagates along the muscle fiber membrane (sarcolemma) and into "
        "T-tubules, triggering calcium release and muscle contraction."
    )
}

app_ui = ui.page_navbar(
    ui.nav_panel(
        "Home",
        ui.div(
            ui.head_content(
                # Script per le animazioni Lottie (già presente)
                ui.HTML('<script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>'),
                ui.tags.script(src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js")
            ),
            ui.h1("Human physiology can be cool", style="margin-bottom: 40px; font-weight: 700; color: #2C3E50;"),
            ui.div(
                ui.div(
                    ui.img(src="https://raw.githubusercontent.com/DaniloBondi/Fisiologia/main/Leonardo.png", style="width: 60%; height: auto; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.15);"),
                    style="flex: 2; max-width: 600px; display: flex; align-items: center; justify-content: center;"
                ),
                ui.div(
                    ui.HTML('<dotlottie-player src="https://lottie.host/3393aace-8cec-48ca-b8d1-8e3c1ac540bf/lqVDiPrtwb.lottie" background="transparent" speed="1" style="width: 160px; height: 160px;" loop autoplay></dotlottie-player>'),
                    ui.HTML('<dotlottie-player src="https://lottie.host/43c73917-b4d7-40ae-a7a2-2ecb34516ec7/WbmA9GxsDC.lottie" background="transparent" speed="1" style="width: 130px; height: 130px;" loop autoplay></dotlottie-player>'),
                    ui.HTML('<dotlottie-player src="https://lottie.host/8f3717a3-bed3-43d9-bd71-7d4bb7f398a4/DtlrqrSLwK.lottie" background="transparent" speed="1" style="width: 110px; height: 110px;" loop autoplay></dotlottie-player>'),
                    style="flex: 1; display: flex; flex-direction: column; justify-content: space-between; align-items: center; padding: 0; gap: 10px;"
                ),
                style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 40px; width: 100%; max-width: 1100px; margin: 0 auto;"
            ),
            ui.p("Teaching materials and oddities curated by Danilo Bondi", style="margin-top: 50px; font-size: 1.4rem; font-style: italic; color: #5D6D7E;"),
            style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; min-height: 90vh; padding: 30px;"
        )
    ),
    ui.nav_panel(
        "Action Potential",
        ui.navset_card_pill(
            ui.nav_panel(
                "Static Comparison",
                ui.layout_sidebar(
                    ui.sidebar(
                        ui.input_select("tissue_type", "Select Tissue Type:", choices={"cardiac": "Cardiac Muscle", "neuron": "Neuron", "skeletal": "Skeletal Muscle"}),
                        ui.input_slider("duration", "Time Window (ms):", min=50, max=500, value=300, step=10)
                    ),
                    ui.card(ui.card_header("Static Waveform"), ui.output_ui("action_potential_plot")),
                    ui.card(ui.card_header("Description"), ui.output_text("description"))
                )
            ),
            ui.nav_panel(
                "Interactive Animation",
                ui.layout_sidebar(
                    ui.sidebar(
                        ui.input_select("stimulus", "Stimulus Potential:", choices={"-60": "-60 mV (Sub-threshold)", "-40": "-40 mV (Above threshold)", "+10": "+10 mV (Above threshold)"}),
                        ui.input_action_button("play", "Generate Animation", class_="btn-primary w-100")
                    ),
                    ui.card(
                        ui.card_header("Neuronal AP Animation"),
                        ui.output_ui("animation_plot"),
                        ui.markdown("**Legend:**\n- Blue dashed line: Activation Threshold (-55 mV)\n- Use the Play/Pause buttons inside the chart to control flow.")
                    )
                )
            )
        )
    ),
    ui.nav_panel(
        "Heart Rate",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_slider("heart_rate", "Heart Rate (bpm):", min=30, max=230, value=70, step=1),
                ui.input_slider("hrv_sdnn", "Heart Rate Variability - SDNN (ms):", min=0, max=100, value=50, step=1),
                ui.input_slider("time_window", "Time Window (seconds):", min=5, max=30, value=10, step=5)
            ),
            ui.card(ui.card_header("ECG Signal Simulation"), ui.output_ui("ecg_plot")),
            ui.card(ui.card_header("Heart Rate Statistics"), ui.output_text("hr_stats"))
        )
    ),
    ui.nav_panel(
        "Ventilation",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_slider("respiratory_rate", ui.HTML("Respiratory Frequency (bpm): <span style='font-size: 0.85em; color: #27AE60;'>12-20 = resting values</span>"), min=0, max=70, value=15, step=1),
                ui.input_slider("tidal_volume", "Tidal Volume (L):", min=0, max=3, value=0.5, step=0.05),
                ui.input_slider("time_window_vent", "Time Window (seconds):", min=10, max=60, value=30, step=5)
            ),
            ui.card(ui.card_header("Respiration Signal"), ui.output_ui("ventilation_plot")),
            ui.card(ui.card_header("Ventilation Statistics"), ui.output_text("ventilation_stats"))
        )
    ),
    
    ui.nav_panel(
        "About",
        ui.card(
            ui.card_header("About This Application"),
            ui.markdown(r"""
                This application simulates action potentials and heart rate patterns in different conditions.
                
                ### Pages:
                - **Action Potential**: Simulates action potentials across different tissue types.
                - **Heart Rate**: Displays simulated ECG signals showing heart rate patterns with customizable heart rate and heart rate variability (SDNN).
                
                In this model, **RMSSD** is derived as a function of **SDNN**, assuming a stationary first-order autoregressive process with **r** set by default to **0.80**, according to the following analytical relationship:
                
                $$RMSSD \approx \sqrt{2 \cdot SDNN^2 \cdot (1 - r_1)}$$
                
                - **Ventilation**: Simulates respiratory signals.
                
                ---
                
                Developed to make human physiology concepts more accessible and engaging. Feel free to use this material however you like; it belongs to everyone and there's no need to credit the authors. However, should you claim it as your own creation and property, I shall feel free to kill you.
                
                ### Credits:
                - [GitHub](https://github.com)
                - [Shiny for Python](https://shiny.posit.co/py/)
                - [Google Gemini](https://gemini.google.com)
                - [LottieFiles](https://lottiefiles.com)
                
                AI is amazing! Thanks to Shiny Assistant, GitHub Copilot, and Gemini, even a 'dummy coder' like me managed to build this website... Feel free to use it however you like; however, it shall feel free to kill you...
                """
            )
        )
    ),
    title=ui.tags.span(
        "Human physiology and beyond",
        style="font-family: 'Aptos', 'Segoe UI', 'Calibri', sans-serif; font-weight: 600;"
    ),
    id="page"
)

# --- SUPPORT FUNCTIONS ---
def generate_cardiac_ap(t):
    v = np.full_like(t, -90.0)
    v[(t >= 10) & (t < 12)] = -90 + (t[(t >= 10) & (t < 12)] - 10) * 65
    v[(t >= 12) & (t < 15)] = 40 - (t[(t >= 12) & (t < 15)] - 12) * 10
    v[(t >= 15) & (t < 210)] = 10
    v[(t >= 210) & (t < 260)] = 10 - (t[(t >= 210) & (t < 260)] - 210) * 2
    return v

def generate_neuron_ap_static(t):
    v = np.full_like(t, -70.0)
    v[(t >= 10) & (t < 11)] = -70 + (t[(t >= 10) & (t < 11)] - 10) * 110
    v[(t >= 11) & (t < 13)] = 40 - (t[(t >= 11) & (t < 13)] - 11) * 55
    v[(t >= 13) & (t < 15)] = -70 - (t[(t >= 13) & (t < 15)] - 13) * 10
    return v

def generate_neuron_ap_animated(t, stimulus_potential):
    v = np.full_like(t, -70.0)
    if stimulus_potential >= -55:
        v[(t >= 10) & (t < 11)] = -70 + (t[(t >= 10) & (t < 11)] - 10) * 110
        v[(t >= 11) & (t < 13)] = 40 - (t[(t >= 11) & (t < 13)] - 11) * 55
        v[(t >= 13) & (t < 15)] = -70 - (t[(t >= 13) & (t < 15)] - 13) * 10
    else:
        v[(t >= 10) & (t < 11)] = -70 + (t[(t >= 10) & (t < 11)] - 10) * 10
        v[(t >= 11) & (t < 12)] = -60 - (t[(t >= 11) & (t < 12)] - 11) * 10
    return v

def generate_skeletal_ap(t):
    v = np.full_like(t, -90.0)
    v[(t >= 10) & (t < 12)] = -90 + (t[(t >= 10) & (t < 12)] - 10) * 65
    v[(t >= 12) & (t < 15)] = 40 - (t[(t >= 12) & (t < 15)] - 12) * 36.67
    return v

def create_plotly_figure(x, y, title, xlabel, ylabel, color='#2E86AB'):
    fig = go.Figure(go.Scatter(x=x, y=y, mode='lines', line=dict(color=color, width=2)))
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel, plot_bgcolor='white', height=450)
    return fig

def generate_ecg_beat(t_beat):
    signal = 0.15 * np.exp(-((t_beat - 0.13) ** 2) / (2 * 0.067 ** 2))
    signal -= 0.05 * np.exp(-((t_beat - 0.27) ** 2) / (2 * 0.017 ** 2))
    signal += 1.0 * np.exp(-((t_beat - 0.30) ** 2) / (2 * 0.017 ** 2))
    signal -= 0.15 * np.exp(-((t_beat - 0.33) ** 2) / (2 * 0.017 ** 2))
    signal += 0.25 * np.exp(-((t_beat - 0.58) ** 2) / (2 * 0.13 ** 2))
    return signal

def generate_respiration_cycle(t_cycle, tidal_volume):
    tv_ml = tidal_volume * 1000
    return (tv_ml / 2) * (1 - np.cos(2 * np.pi * t_cycle))

# --- SERVER ---
def server(input, output, session):
    
    # Gestione reattiva sicura degli intervalli RR per sessione
    rr_intervals = reactive.Value([])

    @render.ui
    def action_potential_plot():
        tissue = input.tissue_type()
        t = np.linspace(0, input.duration(), 1000)
        ap_map = {"cardiac": generate_cardiac_ap, "neuron": generate_neuron_ap_static, "skeletal": generate_skeletal_ap}
        v = ap_map[tissue](t)
        fig = create_plotly_figure(t, v, f'Action Potential: {tissue.title()}', 'Time (ms)', 'Membrane Potential (mV)')
        return ui.HTML(fig.to_html(include_plotlyjs="cdn", full_html=False))

    @render.text
    def description():
        return TISSUE_DESCRIPTIONS[input.tissue_type()]

    @render.ui
    def animation_plot():
        input.play()
        stimulus = int(input.stimulus())
        t = np.linspace(0, 30, 200)
        v = generate_neuron_ap_animated(t, stimulus)
        fig = go.Figure(
            data=[go.Scatter(x=[t[0]], y=[v[0]], mode="lines", line=dict(width=3, color="#E63946"), name="Potential")],
            layout=go.Layout(
                xaxis=dict(range=[0, 30], title="Time (ms)"),
                yaxis=dict(range=[-100, 60], title="Membrane Potential (mV)"),
                plot_bgcolor='white',
                updatemenus=[dict(type="buttons", buttons=[
                    dict(label="▶ Play", method="animate", args=[None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True}]),
                    dict(label="Pause", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])
                ])]
            ),
            frames=[go.Frame(data=[go.Scatter(x=t[:i], y=v[:i])]) for i in range(1, len(t), 3)]
        )
        fig.add_hline(y=-55, line_dash="dash", line_color="#2E86AB", annotation_text="Threshold (-55 mV)")
        return ui.HTML(fig.to_html(include_plotlyjs="cdn", full_html=False))

    @render.ui
    def ecg_plot():
        hr = input.heart_rate()
        target_sdnn = input.hrv_sdnn() / 1000.0  # da ms a secondi
        mean_interval = 60.0 / hr
        t_max = input.time_window()
        
        # 1. Calcoliamo ESATTAMENTE quanti intervalli RR interi stanno nella finestra
        available_time = t_max - 0.5
        
        if available_time <= 0:
            n_beats = 1
        else:
            n_beats = int(available_time / mean_interval)
            
        # Ci servono almeno 2 intervalli per calcolare una deviazione standard!
        n_beats = max(2, n_beats)
        
        # 2. Generiamo rumore autocorrelato per abbattere l'RMSSD
        alpha = 0.80
        raw_noise = np.zeros(n_beats)
        raw_noise[0] = np.random.normal(0, 1)
        for i in range(1, n_beats):
            raw_noise[i] = alpha * raw_noise[i-1] + (1 - alpha) * np.random.normal(0, 1)
            
        # 3. Normalizzazione forzata
        final_noise = (raw_noise - np.mean(raw_noise)) / np.std(raw_noise)
        
        # 4. Applichiamo i target e blocchiamo in limiti fisiologici
        rr_array = mean_interval + (final_noise * target_sdnn)
        rr_array = np.clip(rr_array, 0.2, 2.0) 
        
        # 5. Tracciamo il segnale
        t = np.linspace(0, t_max, int(t_max * 1000))
        ecg_signal = np.zeros_like(t)
        
        curr_time = 0.5
        current_rr_list = []
        
        for interval in rr_array:
            mask = (t >= curr_time) & (t < curr_time + 0.6)
            if np.any(mask):
                ecg_signal[mask] += generate_ecg_beat((t[mask] - curr_time) / 0.6)
                
            current_rr_list.append(interval * 1000)
            curr_time += interval
            
        # Inviamo al pannello statistiche SOLO gli intervalli realmente disegnati
        rr_intervals.set(current_rr_list)
        
        fig = create_plotly_figure(t, ecg_signal, "ECG Simulation", "Time (s)", "Voltage (mV)", "#E63946")
        return ui.HTML(fig.to_html(include_plotlyjs="cdn", full_html=False))

    @render.text
    def hr_stats():
        target_sdnn = input.hrv_sdnn()
        intervals = rr_intervals.get()
        
        if len(intervals) > 1:
            actual_sdnn = np.std(intervals)
            successive_diffs = np.diff(intervals)
            actual_rmssd = np.sqrt(np.mean(successive_diffs ** 2))
        else:
            actual_sdnn = actual_rmssd = 0
            
        return (f"Heart Rate: {input.heart_rate()} bpm\n"
                f"Target SDNN (Slider): {target_sdnn} ms\n"
                f"Measured RMSSD: {actual_rmssd:.1f} ms")

    @render.ui
    def ventilation_plot():
        rf = input.respiratory_rate()
        tv = input.tidal_volume()
        tw = input.time_window_vent()
        
        if rf == 0:
            t = np.linspace(0, tw, 1000); volume = np.zeros_like(t)
        else:
            breath_period = 60.0 / rf
            t = np.linspace(0, tw, int(tw * 100))
            volume = np.zeros_like(t)
            for b_start in np.arange(0, tw, breath_period):
                mask = (t >= b_start) & (t < b_start + breath_period)
                if np.any(mask):
                    t_norm = (t[mask] - b_start) / breath_period
                    volume[mask] = generate_respiration_cycle(t_norm, tv)
        
        fig = go.Figure(go.Scatter(x=t, y=volume, mode='lines', line=dict(color="#27AE60", width=2)))
        fig.update_layout(title="Respiration Signal", xaxis_title="Time (s)", yaxis_title="Volume (mL)",
                          yaxis=dict(range=[0, 3000]), plot_bgcolor='white', height=450)
        fig.add_hline(y=500, line_dash="dot", line_color="#95A5A6")
        return ui.HTML(fig.to_html(include_plotlyjs="cdn", full_html=False))

    @render.text
    def ventilation_stats():
        rf, tv = input.respiratory_rate(), input.tidal_volume()
        return f"Respiratory Frequency: {rf} bpm\nTidal Volume: {tv:.2f} L\nMinute Ventilation: {rf * tv:.2f} L/min"

app = App(app_ui, server)
