<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="formData.username"
                label="Username"
                required
              ></v-text-field>
            </v-col>

            <v-col cols="12" v-if="!editMode">
              <v-text-field
                v-model="formData.password"
                label="Password"
                type="password"
                required
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-select
                v-model="formData.roles"
                :items="availableRoles"
                label="Roles"
                multiple
                chips
              ></v-select>
            </v-col>

            <v-col cols="12">
              <v-select
                v-model="formData.preferences.timezone"
                :items="timezones"
                label="Timezone"
                required
              ></v-select>
            </v-col>

            <v-col cols="12">
              <v-switch
                v-model="formData.active"
                label="Active"
              ></v-switch>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="blue darken-1"
          text
          @click="close"
        >
          Cancel
        </v-btn>
        <v-btn
          color="blue darken-1"
          text
          @click="save"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'UserDialog',

  props: {
    value: Boolean,
    user: Object
  },

  data: () => ({
    formData: {
      username: '',
      password: '',
      roles: [],
      preferences: {
        timezone: ''
      },
      active: true
    },
    availableRoles: ['admin', 'manager', 'tester'],
    timezones: [
      'America/New_York',
      'Europe/London',
      'Asia/Tokyo',
      'Australia/Sydney'
    ]
  }),

  computed: {
    dialog: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      }
    },
    formTitle() {
      return this.user ? 'Edit User' : 'New User'
    },
    editMode() {
      return !!this.user
    }
  },

  watch: {
    user: {
      handler(user) {
        if (user) {