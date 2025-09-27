useEffect(() => {
  const fetchData = async () => {
    try {
      setLoading(true);
      console.log('🔄 Starting API calls...');
      
      // Test each API endpoint individually to see which one fails
      try {
        const providersResponse = await getProviders();
        console.log('✅ Providers API success');
      } catch (err) {
        console.error('❌ Providers API failed:', err);
      }
      
      try {
        const bundlesResponse = await getBundles();
        console.log('✅ Bundles API success');
      } catch (err) {
        console.error('❌ Bundles API failed:', err);
      }
      
      try {
        const routersResponse = await getRouters();
        console.log('✅ Routers API success');
      } catch (err) {
        console.error('❌ Routers API failed:', err);
      }
      
      // Now try to fetch all data
      const [providersResponse, bundlesResponse, routersResponse] = await Promise.allSettled([
        getProviders(),
        getBundles(),
        getRouters()
      ]);
      
      console.log('All API responses:', { providersResponse, bundlesResponse, routersResponse });
      
      // Handle settled promises
      const providersData = providersResponse.status === 'fulfilled' && Array.isArray(providersResponse.value?.data) 
        ? providersResponse.value.data 
        : [];
      
      const bundlesData = bundlesResponse.status === 'fulfilled' && Array.isArray(bundlesResponse.value?.data) 
        ? bundlesResponse.value.data 
        : [];
      
      const routersData = routersResponse.status === 'fulfilled' && Array.isArray(routersResponse.value?.data) 
        ? routersResponse.value.data 
        : [];
      
      console.log('📊 Final data:', {
        providers: providersData.length,
        bundles: bundlesData.length,
        routers: routersData.length
      });
      
      setProviders(providersData);
      setBundles(bundlesData);
      setRouters(routersData);
      setLoading(false);
      
    } catch (err) {
      console.error('💥 General error in fetchData:', err);
      setError('Failed to load data. Please check the console for details.');
      setLoading(false);
    }
  };

  fetchData();
}, []);