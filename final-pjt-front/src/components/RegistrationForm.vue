<template>
  <div class="registration-form">
    <div>
      <v-text-field
        v-model="credentials.username"
        :rules="nameRules"
        :counter="20"
        label="User Name"
        required
      ></v-text-field>
    </div>
    <div>
      <v-text-field
        v-model="credentials.password"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="[rules.required, rules.min]"
        :type="show1 ? 'text' : 'password'"
        counter
        hint="At least 8 characters"
        label="Password"
        required
        @click:append="show1 = !show1"
      ></v-text-field>
    </div>
    <div>
      <v-text-field
        v-model="credentials.confirm_password"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="[rules.required, rules.min]"
        :type="show1 ? 'text' : 'password'"
        counter
        hint="At least 8 characters"
        label="confirm-password"
        required
        @click:append="show1 = !show1"
      ></v-text-field>
    </div>
    <div>
      <v-btn block @click="doRegistration(credentials)">submit</v-btn>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "RegistrationForm",
  data: function () {
    return {
      show1: false,
      nameRules: [
        (v) => !!v || "Name is required",
        (v) => v.length <= 20 || "Name must be less than 20 characters",
      ],
      rules: {
        required: (value) => !!value || "Required.",
        min: (v) => v.length >= 8 || "Min 8 characters",
      },
      credentials: {
        username: "",
        password: "",
        confirm_password: "",
      },
    };
  },
  methods: {
    ...mapActions(["doRegistration"]),
  },
};
</script>

<style></style>
