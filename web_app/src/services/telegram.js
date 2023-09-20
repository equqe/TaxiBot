export const sendHapticFeedback = () => {
    try {
        window.Telegram.WebApp.HapticFeedback.impactOccurred("medium");
    }catch (e) {
        console.warn(e);
    }
}
