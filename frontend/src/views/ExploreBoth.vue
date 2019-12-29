<template>
  <div>
    <h1>Explore Both</h1>
    <outdated-agreement-warning/>
  </div>
</template>

<script>
// import FuzzyAutoComplete from '@/components/FuzzyAutoComplete';
import OutdatedAgreementWarning from '@/components/OutdatedAgreementWarning';
import MemoizedAssistAPI from '@/pseudo-assist-api.js';

export default {
  name: 'ExploreBoth',
  components: {
    // FuzzyAutoComplete,
    OutdatedAgreementWarning
  },
};
</script>