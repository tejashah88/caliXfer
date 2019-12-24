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
            img="https://www.midlandstech.edu/sites/default/files/bc_8182.jpg"
            description="I know my college and major, but I don't know my requirements needed to transfer..."
            route="transfer-reqs"
            max-width=400>
          </HomeTile>
        </v-col>

        <v-col>
          <HomeTile
            title="Explore different majors"
            img="https://zen.collegevine.com/wp-content/uploads/2016/07/college-majors-istock_000017855571xlarge-1280x640.jpg"
            description="I know which college I want to attend, but I'm not sure which major is right for me..."
            route="explore-majors"
            max-width=400>
          </HomeTile>
        </v-col>

        <v-col>
          <HomeTile
            title="Explore different universities"
            img="https://www.southwestjournal.com/wp-content/uploads/2017/05/Walsh0518web.jpg"
            description="I know which major that I want to study, but I'm not sure which college is right for me..."
            route="explore-universities"
            max-width=400>
          </HomeTile>
        </v-col>

        <v-col>
          <HomeTile
            title="Explore majors and universities"
            img="https://www.everystudent.com/3/share2019/universe2.jpg"
            description="I don't know which college to attend and which major to study..."
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