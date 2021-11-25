<template>
  <v-container>
    <RegistrationForm></RegistrationForm>
  </v-container>
</template>

<script>
import RegistrationForm from "@/components/RegistrationForm.vue";
import { mapActions } from "vuex";

export default {
  name: "Registration",
  components: { RegistrationForm },
  methods: {
    ...mapActions(["setAppTitle"]),
  },
  created: function () {
    this.setAppTitle("Registration");
  },
};
</script>
