package eoc21.client;

import java.util.ArrayList;

import com.smartgwt.client.widgets.layout.HLayout;
import com.smartgwt.client.widgets.layout.SectionStack;

/**
 * This class takes care of all the additional widgets making up my website, including, their
 * location and size.
 * @author ed
 *
 */

//Should be a singleton class.
public class LayoutManager4Website {
	private static HLayout layout; ;
	private static final LayoutManager4Website LAYOUT_MANAGER_INSTANCE = new LayoutManager4Website();

	private LayoutManager4Website() {
		
	}
	 
	   public static LayoutManager4Website getInstance(ArrayList<SectionStack> websiteSections) {
		   //Add layout info here.
		   layout = new HLayout();
		   layout.setMembersMargin(20);
		   for(SectionStack s: websiteSections){
			   layout.addMember(s);
		   }
	      return LAYOUT_MANAGER_INSTANCE;
	   }
	   
	  public HLayout getHLayout(){
		  return LayoutManager4Website.layout;
	  }
	
	
}
