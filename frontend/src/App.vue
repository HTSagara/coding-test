//frontend/src/App.vue
<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>User Management System</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',
}
</script>
