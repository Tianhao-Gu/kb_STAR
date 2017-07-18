/*
   Name of module: STAR

   This KBase module wraps the free open source software STAR: ultrafast universal RNA-seq aligner.
   STAR-2.5.3a

   References:
   https://github.com/alexdobin/STAR/
   https://github.com/alexdobin/STAR/blob/master/doc/STARmanual.pdf
*/

module STAR {
    /* 
        A 'typedef' allows you to provide a more specific name for
        a type.  Built-in primitive types include 'string', 'int',
        'float'.  Here we define a type named assembly_ref to indicate
        a string that should be set to a KBase ID reference to an
        Assembly data object.
    */
    typedef string assembly_ref;

    /* A boolean - 0 for false, 1 for true.
        @range (0, 1)
    */
		    
    typedef int bool;

	        /* An X/Y/Z style reference
    */
    typedef string obj_ref;

    /*
	Will align the input reads (or set of reads specified in a SampleSet) to the specified
        assembly or assembly for the specified Genome (accepts Assembly, ContigSet, or Genome types)
        and produces a ReadsAlignment object, or in the case of a SampleSet, a ReadsAlignmentSet
        object

	obj_ref genome_ref: KBase workspace reference Genome
	obj_ref readsset_ref: the workspace reference for the set of reads to align, referring to 
		either a SingleEnd/PairedEnd reads, or a ReadsSet input
	string output_workspace - name or id of the WS to save the results to, provided by the narrative for housing output in KBase
	string output_name - name of the output ReadsAlignment or ReadsAlignmentSet object
        int runThreadN - the number of threads for STAR to use (default to 2)	
	string outFileNamePrefix: you can change the file prefixes using --outFileNamePrefix /path/to/output/dir/prefix
                By default, this parameter is ./, i.e. all output files are written in current directory without a prefix
	string quantMode: types of quantification requested--none/TranscriptomeSAM/GeneCounts
	int outFilterMultimapNmax: max number of multiple alignments allowed for a read: if exceeded, 
		the read is considered unmapped, default to 20
	int alignSJoverhangMin: minimum overhang for unannotated junctions, default to 8
	int alignSJDBoverhangMin: minimum overhang for annotated junctions, default to 1
	int outFilterMismatchNmax: maximum number of mismatches per pair, large number switches off this filter, default to 999
	int alignIntronMin: minimum intron length, default to 20
	int alignIntronMax: maximum intron length, default to 1000000
	int alignMatesGapMax: maximum genomic distance between mates, default to 1000000
        create_report = 1 if we build a report, 0 otherwise. (default 1) (shouldn not be user set - mainly used for subtasks)
	
        @optional outFilterType
        @optional outFilterMultimapNmax
        @optional outSAMtype
        @optional outSAMattrIHstart
        @optional outSAMstrandField
	@optional quantMode
	@optional alignSJoverhangMin
	@optional alignSJDBoverhangMin
	@optional outFilterMismatchNmax	
	@optional alignIntronMin
	@optional alignIntronMax
	@optional alignMatesGapMax
	@optional outFileNamePrefix
    */
    typedef structure {
        obj_ref readsset_ref;
        obj_ref genome_ref;
        string output_workspace;
        int runThreadN;
	string output_name;
        string condition; 
        string outFilterType;
        string outSAMtype;
        int outSAMattrIHstart;
        string outSAMstrandField;
	string quantMode;
	int outFilterMultimapNmax;
	int alignSJoverhangMin;
	int alignSJDBoverhangMin;
	int outFilterMismatchNmax;
	int alignIntronMin;
	int alignIntronMax;
	int alignMatesGapMax;
	string outFileNamePrefix;
                
        int concurrent_njsw_tasks;
        int concurrent_local_tasks;
        bool create_report;
    } AlignReadsParams;

    /*
        Here is the definition of the output of the function.  The output
        can be used by other SDK modules which call your code, or the output
        visualizations in the Narrative.  'report_name' and 'report_ref' are
        special output fields- if defined, the Narrative can automatically
        render your Report.

        alignment_ref: can be either an Alignment or AlignmentSet, depending on inputs.			
        report_name: report name generated by KBaseReport
        report_ref: report reference generated by KBaseReport
    */
    typedef structure {
        obj_ref alignment_ref;
        string report_name;
        string report_ref;
    } AlignReadsResult;
   
    funcdef align_reads_to_assembly_app(AlignReadsParams params)
        returns (AlignReadsResult result) authentication required;

    /* aligns a single reads object to produce */
    funcdef align_one_reads_to_assembly()
        returns () authentication required;
 
    /*
        The actual function is declared using 'funcdef' to specify the name
        and input/return arguments to the function.  For all typical KBase
        Apps that run in the Narrative, your function should have the 
        'authentication required' modifier.
    */
    funcdef run_star(AlignReadsParams params)
        returns (AlignReadsResult returnVal) authentication required;

    /* Provide a reference to either an Assembly or Genome to get a STAR index.

       output_dir is optional, if provided the index files will be saved in that
       directory.  If not, a directory will be generated for you and returned
       by this function.  If specifying the output_dir, the directory must not
       exist yet (to ensure only the index files are added there).
        
       Currently, STAR indexes are cached to a WS object.  If that object does
       not exist, then calling this function can create a new object.  To create
       the cache, you must specify the ws name or ID in 'ws_for_cache' in which
       to create the cached index.  If this field is not set, the result will
       not be cached.  This parameter will eventually be deprecated once the
       big file cache service is implemented.
    */
    typedef structure {
        string ref;
        string output_dir;
        string ws_for_cache;
    } GetSTARIndex;

    /*
        output_dir - the folder containing the index files
        from_cache - 0 if the index was built fresh, 1 if it was found in the cache
        pushed_to_cache - if the index was rebuilt and successfully added to the
                          cache, this will be set to 1; otherwise set to 0
    */
    typedef structure {
        string output_dir;
        bool from_cache;
        bool pushed_to_cache;
    } GetSTARIndexResult;


    funcdef get_star_index(GetSTARIndex params)
        returns(GetSTARIndexResult result) authentication required;
};
