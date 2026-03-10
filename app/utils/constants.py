"""Vocald - App-Wide Constants"""

APP_NAME        = 'Vocald'
APP_VERSION     = '1.0.0'
APP_PACKAGE     = 'com.vocald.speakerid'

# Processing
MAX_RETRIES         = 3
BATTERY_THRESHOLD   = 15       # Pause processing below this %
MAX_CENTROIDS       = 5        # Max voice centroids per speaker
EMBEDDING_DIM       = 192      # ECAPA-TDNN output dimensions

# Monitoring
WORKMANAGER_INTERVAL_MIN = 15  # Minutes between background checks

# Audio
SUPPORTED_FORMATS   = ['.mp3', '.wav', '.m4a', '.ogg', '.aac', '.opus', '.flac']
SAMPLE_RATE         = 16000    # Hz - required by ECAPA-TDNN
CHUNK_DURATION_SEC  = 30       # Seconds per processing chunk

# Database
DB_NAME             = 'vocald.db'
DB_VERSION          = 1

# UI
SPLASH_DURATION_SEC = 2.5