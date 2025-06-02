from pydub import AudioSegment

song = AudioSegment.from_mp3("audios/audio1.mp3")

# Start time in milliseconds: 2 minutes and 15 seconds
start_time = 2 * 60 * 1000 + 15 * 1000  # = 135000 ms

# Slice from 2:15 until the end
cut = song[start_time:]

# Export the cut segment
cut.export("recortes/audio1_cut.mp3", format="mp3")