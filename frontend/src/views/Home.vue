<template>
  <div>
    <v-col
      cols="auto"
      lg="10"
      xl="6"
      offset="0"
      offset-lg="2"
      offset-xl="3">
      <v-row>
        <v-col>
          <HomeTile
            title="Check transfer requirements"
            img="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
            description="I know my college and major, but I don't know my requirements needed to transfer..."
            route="transfer-reqs"
            max-width=400>
          </HomeTile>
        </v-col>

        <v-col>
          <HomeTile
            title="Explore different majors"
            img="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
            description="I know which college I want to attend, but I'm not sure which major is right for me..."
            route="explore-majors"
            max-width=400>
          </HomeTile>
        </v-col>

        <v-col>
          <HomeTile
            title="Explore different universities"
            img="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
            description="I know which major that I want to study, but I'm not sure which college is right for me..."
            route="explore-universities"
            max-width=400>
          </HomeTile>
        </v-col>

        <v-col>
          <HomeTile
            title="About the project"
            img="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
            description="Check out what this website is all about, and what you can do with it!"
            route="about"
            max-width=400>
          </HomeTile>
        </v-col>
      </v-row>
    </v-col>
  </div>
</template>

<script>

import HomeTile from '@/components/HomeTile';

export default {
  name: 'Home',
  components: {
    HomeTile
  }
};
</script>