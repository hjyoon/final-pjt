<template>
  <v-app>
    <AppBar></AppBar>
    <NavigationDrawer></NavigationDrawer>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import { mapActions } from "vuex";
import AppBar from "@/components/AppBar.vue";
import NavigationDrawer from "@/components/NavigationDrawer.vue";

export default {
  name: "App",
  components: { AppBar, NavigationDrawer },
  data: () => ({}),
  methods: {
    ...mapActions(["doAutoLogin"]),
  },
  created: function () {
    this.doAutoLogin();
  },
};
</script>
