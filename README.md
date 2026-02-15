# performance-intelligence
<template>
  <div id="app">
    <button 
      @click="toggleState" 
      :class="{ 'active': isOn, 'inactive': !isOn }"
    >
      {{ isOn ? 'ON' : 'OFF' }}
    </button>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      // Initialize as true so it matches the 'ON' state in your screenshot
      isOn: true
    };
  },
  methods: {
    toggleState() {
      this.isOn = !this.isOn;
    }
  }
};
</script>

<style>
/* Basic reset to center content for presentation */
body {
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f4f9;
  font-family: sans-serif;
}

#app {
  text-align: center;
}

/* Base button styles */
button {
  font-size: 1.5rem;
  font-weight: bold;
  padding: 15px 40px;
  border: none;
  border-radius: 50px; /* Pill shape */
  cursor: pointer;
  color: white;
  transition: all 0.3s ease; /* Smooth transition for color changes */
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  outline: none;
  min-width: 120px; /* Ensures button doesn't resize drastically between texts */
}

/* State: ON */
button.active {
  background-color: #4CAF50; /* Green */
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4); /* Green glow */
}

/* State: OFF */
button.inactive {
  background-color: #ff5252; /* Red */
  box-shadow: 0 4px 15px rgba(255, 82, 82, 0.4); /* Red glow */
  opacity: 0.8;
}

/* Optional: Button press effect */
button:active {
  transform: scale(0.95);
}
</style>
