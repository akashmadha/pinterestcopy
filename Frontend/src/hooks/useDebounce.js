// ✅ Import React hooks
import { useEffect, useState } from "react";

// ✅ Export a reusable custom hook
// It takes any value (string, number, object, etc.) and a delay (default 350ms)
export default function useDebounce(value, delay = 350) {
  // 🧠 Create internal state to store the "debounced" version of the value
  // Initially, it’s just equal to the current value
  const [debounced, setDebounced] = useState(value);

  // 🕓 useEffect runs every time `value` or `delay` changes
  useEffect(() => {
    // ⏱️ Create a timer: after `delay` ms, update the debounced value
    const t = setTimeout(() => setDebounced(value), delay);

    // 🧹 Cleanup function:
    // If `value` changes again before the delay finishes,
    // this clears the previous timer (so it doesn’t update too early)
    return () => clearTimeout(t);

    // Dependencies: rerun effect whenever `value` or `delay` changes
  }, [value, delay]);

  // 🎯 Return the debounced (delayed) value
  return debounced;
}
